from pathlib import Path
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from src import paths
from src.paths import BARCODES_DIR
from src.paths import USED_DIR

from src.Utils.Utilities import Utilities
from src.Utils.Validator import Validator, handle_validation_errors
from src.Utils.Exceptions import ValidationError

from src.model.PdfFile import PdfFile

from src.view.pages.MainPage import MainPage
from src.view.ui_notifications import show_dialog, show_loading_dialog, close_loading_dialog


class MainPageController:
    """
    Контроллер главной страницы приложения.

    Управляет взаимодействием с главной страницей, выбором директорий и обработкой PDF файлов со штрихкодами.
    """
    # Константы для расчета размера и позиции штрихкода
    BARCODE_WIDTH_FACTOR: float = 5.0
    BARCODE_HEIGHT_FACTOR: float = 20.0
    # Максимальное количество потоков для обработки файлов
    MAX_WORKERS: int = 4

    def __init__(self, app_controller: 'MainController') -> None:
        """
        Инициализация контроллера главной страницы.

        Args:
            app_controller (MainController): Главный контроллер приложения.
        """
        self.app_controller: 'MainController' = app_controller
        self.picker_service = app_controller.picker_service
        self.barcodes_count: int = -1
        self.view: MainPage = MainPage(self)

        self._update_barcodes_count()

    @staticmethod
    def open_archive() -> None:
        """
        Открывает директорию с отработанными файлами.
        """
        Utilities.open_folder(USED_DIR)

    def pick_directory(self, target_widget: 'ft.TextField') -> None:
        """
        Обрабатывает выбор директории и сохраняет путь.

        Args:
            target_widget (ft. TextField): Поле ввода, в которое будет записан путь к директории.
        """

        def callback(path: str) -> None:
            if target_widget == self.view.folder_path_field:
                self.view.folder_path_field.value = path
            elif target_widget == self.view.output_folder_field:
                self.view.output_folder_field.value = path

        self.picker_service.pick_directory(target_widget, callback)

    def _update_barcodes_count(self) -> None:
        """
        Обновляет количество штрихкодов в интерфейсе.

        Raises:
            ValueError: Если не удалось подсчитать количество штрихкодов из-за ошибки доступа к директории.
        """
        try:
            self.barcodes_count = Utilities.count_files_by_extension(BARCODES_DIR, '.png')
            self.view.barcode_count_text.value = f"Свободные штрихкоды: {self.barcodes_count}"
            self.app_controller.page.update()
        except ValueError as e:
            show_dialog(self.app_controller.page, "Ошибка", f"Не удалось обновить количество штрихкодов: {e}")

    def _process_single_pdf(self, pdf_path: str, barcode_image: str, output_path: str) -> None:
        """
        Обрабатывает один PDF файл и прикрепляет к нему штрихкод.
        
        Args:
            pdf_path (str): Путь к PDF файлу.
            barcode_image (str): Путь к изображению штрихкода.
            output_path (str): Путь сохранения обработанного PDF.
            
        Raises:
            Exception: Если произошла ошибка при обработке файла.
        """
        pdf_processor: PdfFile = PdfFile(pdf_path)
        width, height = pdf_processor.get_first_page_size()

        # Расчет позиции и размера штрихкода
        x_size: float = width / self.BARCODE_WIDTH_FACTOR
        y_size: float = height / self.BARCODE_HEIGHT_FACTOR
        x_pos: float = width - x_size
        y_pos: float = height - y_size

        pdf_processor.insert_image_on_first_page(
            image_path=barcode_image,
            output_pdf_path=Path(output_path) / f"{Path(pdf_path).stem}_{Path(barcode_image).stem}.pdf",
            x=x_pos,
            y=y_pos,
            width=x_size,
            height=y_size
        )
        Utilities.create_directory(paths.USED_PDFS_DIR, paths.USED_BARCODES_DIR)
        Utilities.move_file(pdf_path, paths.USED_PDFS_DIR)
        Utilities.move_file(barcode_image, paths.USED_BARCODES_DIR)

    @handle_validation_errors
    def process_pdfs(self) -> None:
        """
        Прикрепляет штрихкоды к PDF файлам с использованием многопоточности.

        Извлекает PDF файлы и штрихкоды из указанных директорий, добавляет штрихкоды на первые страницы PDF
        и перемещает использованные файлы в соответствующие папки. Операции выполняются параллельно.

        Raises:
            ValidationError: Если директории не указаны или недоступны.
            RuntimeError: Если произошла ошибка при обработке файлов.
        """
        pdf_folder: str = self.view.folder_path_field.value
        output_path: str = self.view.output_folder_field.value

        if not pdf_folder or not output_path:
            raise ValidationError("Не указаны директории с PDF файлами и для сохранения")

        if not Validator.is_directory_exists(pdf_folder):
            raise ValidationError("Директория с PDF файлами недоступна")
        if not Validator.is_directory_exists(output_path):
            raise ValidationError("Директория для сохранения недоступна")
        if not Validator.is_directory_exists(paths.BARCODES_DIR):
            raise ValidationError("Папка со штрихкодами не найдена")

        barcode_images: List[str] = Utilities.get_files_with_extension(paths.BARCODES_DIR, ".png", ".jpg", ".jpeg")

        if not barcode_images:
            show_dialog(self.app_controller.page, "Ошибка", "Нет штрихкодов в директории")
            return

        pdf_files: List[str] = Utilities.get_files_with_extension(pdf_folder, ".pdf")

        if not pdf_files:
            show_dialog(self.app_controller.page, "Ошибка", "Нет PDF файлов в директории")
            return

        Utilities.create_directory(output_path)

        # Создаем пары PDF-штрихкод для обработки
        pdf_barcode_pairs = list(zip(pdf_files, barcode_images[:len(pdf_files)]))
        total_files = len(pdf_barcode_pairs)
        
        # Показываем диалог загрузки
        loading_dialog = show_loading_dialog(
            self.app_controller.page, 
            f"Обработка файлов (0/{total_files})..."
        )
        
        errors = []
        processed = 0
        
        # Запускаем многопоточную обработку
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            # Создаем задачи для выполнения
            futures = {
                executor.submit(self._process_single_pdf, pdf_path, barcode_image, output_path): 
                (pdf_path, barcode_image) for pdf_path, barcode_image in pdf_barcode_pairs
            }
            
            # Обрабатываем результаты по мере завершения
            for future in as_completed(futures):
                pdf_path, barcode_image = futures[future]
                try:
                    future.result()  # Получаем результат или исключение
                    processed += 1
                    # Обновляем текст диалога
                    loading_dialog.content.controls[1].value = f"Обработка файлов ({processed}/{total_files})..."
                    self.app_controller.page.update()
                except Exception as e:
                    errors.append(f"Ошибка при обработке файла '{pdf_path}' с штрихкодом '{barcode_image}': {e}")
        
        # Закрываем диалог загрузки
        close_loading_dialog(self.app_controller.page, loading_dialog)
        
        # Обрабатываем возможные ошибки
        if errors:
            error_message = "\n".join(errors[:5])
            if len(errors) > 5:
                error_message += f"\n... и еще {len(errors) - 5} ошибок"
            show_dialog(
                self.app_controller.page, 
                "Ошибки при обработке файлов", 
                error_message
            )
        else:
            show_dialog(
                self.app_controller.page,
                title="Успешная обработка PDF файлов",
                content=f"Штрихкоды успешно прикреплены к {processed} PDF файлам"
            )
            
        self._update_barcodes_count()
