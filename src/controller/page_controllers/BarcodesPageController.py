import os

from src.Utils.Exceptions import ValidationError
from src.Utils.Validator import Validator, handle_validation_errors
from src.Utils.Utilities import Utilities

from src.model.ExcelFile import ExcelFile

from src.view.pages.BarcodesPage import BarcodesPage
from src.view.ui_notifications import show_dialog

from src import paths


class BarcodesPageController:
    """
    Контроллер страницы со штрихкодами.

    Управляет взаимодействием со страницей добавления штрихкодов, выбором файлов или директорий
    и извлечением штрихкодов из Excel-файлов.
    """

    def __init__(self, app_controller: 'MainController') -> None:
        """
        Инициализация контроллера страницы штрихкодов.

        Args:
            app_controller (MainController): Главный контроллер приложения.
        """
        self.app_controller: 'MainController' = app_controller
        self.picker_service = app_controller.picker_service
        self.view = BarcodesPage(self)
        self.view.barcodes_count = 0
        self.path = None

    def picker(self, mode: str, target_widget: 'ft.Control') -> None:
        """
        Выбирает файл или директорию и сохраняет путь.

        Args:
            mode (str): Режим выбора ('file' для файла, 'directory' для директории).
            target_widget (ft.Control): Виджет, для которого выполняется выбор.

        Raises:
            ValueError: Если указан неверный режим.
        """

        def callback(path: str) -> None:
            self.path = path

        if mode == "file":
            self.picker_service.pick_file(target_widget, callback)
        elif mode == "directory":
            self.picker_service.pick_directory(target_widget, callback)
        else:
            raise ValueError(f"Неверный режим выбора: {mode}. Ожидается 'file' или 'directory'.")

    @handle_validation_errors
    def process_barcodes(self) -> None:
        """
        Извлекает штрихкоды из выбранного файла или всех Excel-файлов в директории.

        Проверяет выбранный путь, создает директорию для штрихкодов и обрабатывает файлы,
        сохраняя извлеченные штрихкоды в BARCODES_DIR.

        Raises:
            ValidationError: Если путь не выбран, недоступен или содержит ошибки валидации.
            RuntimeError: Если произошла ошибка при обработке файлов.
        """
        # Проверяем, что путь выбран
        if not self.path:
            show_dialog(self.app_controller.page, "Ошибка", "Путь не выбран")
            return

        # Создаем директорию для результатов
        try:
            Utilities.create_directory(paths.BARCODES_DIR)
        except OSError as e:
            raise ValidationError(f"Не удалось создать директорию {paths.BARCODES_DIR}: {e}")

        # Проверяем, файл это или директория
        if os.path.isfile(self.path):
            # Обработка одного файла
            if not Validator.is_excel(self.path):
                raise ValidationError("Выбранный файл не является Excel-файлом")
            try:
                ExcelFile(self.path).process_images_and_text(paths.BARCODES_DIR)
                show_dialog(self.app_controller.page, "Успешно", "Штрихкоды извлечены.")
            except RuntimeError as e:
                raise RuntimeError(f"Ошибка при обработке файла {self.path}: {e}")

        elif os.path.isdir(self.path):
            # Обработка директории
            if not Validator.is_directory_exists(self.path):
                raise ValidationError("Указанная директория недоступна или не существует")

            excel_files: list[str] = Utilities.get_files_with_extension(self.path, ".xlsx", ".xls", ".xlsb")
            if not excel_files:
                show_dialog(self.app_controller.page, "Ошибка", "В указанной директории нет Excel-файлов")
                return

            for excel_file in excel_files:
                try:
                    ExcelFile(excel_file).process_images_and_text(paths.BARCODES_DIR)
                except RuntimeError as e:
                    raise RuntimeError(f"Ошибка при обработке файла {excel_file}: {e}")

            show_dialog(self.app_controller.page, "Успешно", "Все файлы обработаны и сохранены в BARCODES_DIR")

        else:
            raise ValidationError("Выбранный путь не является ни файлом, ни директорией")
