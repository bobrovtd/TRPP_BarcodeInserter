from typing import Tuple
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image as PILImage


class PdfFile:
    """
    Класс для работы с PDF файлами.

    Предоставляет методы для анализа ориентации, получения размеров страницы и вставки изображения
    на первую страницу PDF файла.
    """

    def __init__(self, pdf_path: str) -> None:
        """
        Инициализация PDF процессора.

        Args:
            pdf_path (str): Путь к существующему PDF файлу.

        Raises:
            FileNotFoundError: Если файл по указанному пути не существует.
            PyPDF2.errors.PdfReadError: Если файл не является корректным PDF.
        """
        self.pdf_path: str = pdf_path
        try:
            self.reader: PdfReader = PdfReader(pdf_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{pdf_path}' не найден.")
        except Exception as e:
            raise ValueError(f"Ошибка при чтении PDF файла '{pdf_path}': {str(e)}")

    def is_vertical(self) -> bool:
        """
        Определяет ориентацию первой страницы PDF файла.

        Returns:
            bool: True, если страница вертикальная (высота больше ширины), иначе False.
        """
        first_page = self.reader.pages[0]

        # Получаем размеры страницы
        width: float = first_page.mediabox.width
        height: float = first_page.mediabox.height

        # Определяем ориентацию
        return height > width

    def get_first_page_size(self) -> Tuple[float, float]:
        """
        Возвращает размеры первой страницы PDF файла.

        Returns:
            Tuple[float, float]: Кортеж с шириной и высотой страницы (width, height) в пунктах.
        """
        first_page = self.reader.pages[0]
        width: float = float(first_page.mediabox.width)
        height: float = float(first_page.mediabox.height)
        return width, height

    def insert_image_on_first_page(
            self,
            image_path: str,
            output_pdf_path: str,
            x: float = 0,
            y: float = 0,
            width: float | None = None,
            height: float | None = None
    ) -> None:
        """
        Вставляет изображение на первую страницу существующего PDF файла.

        Args:
            image_path (str): Путь к изображению, которое нужно вставить.
            output_pdf_path (str): Путь к выходному PDF файлу.
            x (float, optional): Координата X для вставки изображения. По умолчанию 0.
            y (float, optional): Координата Y для вставки изображения. По умолчанию 0.
            width (float | None, optional): Ширина изображения (если None, используется значение по умолчанию).
            height (float | None, optional): Высота изображения (если None, используется значение по умолчанию).

        Raises:
            FileNotFoundError: Если изображение не найдено.
            ValueError: Если параметры изображения некорректны.
            IOError: Если не удается сохранить выходной файл.
        """
        # Константы
        DEFAULT_IMAGE_WIDTH: float = 100.0

        # Извлекаем первую страницу
        first_page = self.reader.pages[0]

        # Получаем размеры первой страницы
        page_width, page_height = self.get_first_page_size()

        # Создаем временный PDF с изображением, размер страницы совпадает с исходным PDF
        packet: BytesIO = BytesIO()
        c: canvas.Canvas = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Определяем размеры изображения
        try:
            with PILImage.open(image_path) as img:
                img_width, img_height = img.size
                img_ratio: float = img_width / img_height
        except FileNotFoundError:
            raise FileNotFoundError(f"Изображение '{image_path}' не найдено.")
        except Exception as e:
            raise ValueError(f"Ошибка при открытии изображения '{image_path}': {str(e)}")

        # Устанавливаем размеры изображения, если они не заданы
        if width is None and height is None:
            width = DEFAULT_IMAGE_WIDTH
            height = width / img_ratio
        elif width is None and height is not None:
            width = height * img_ratio
        elif height is None and width is not None:
            height = width / img_ratio

        # Проверка, чтобы изображение не выходило за пределы страницы
        if x + width > page_width:
            width = page_width - x
            height = width / img_ratio
        if y + height > page_height:
            height = page_height - y
            width = height * img_ratio

        # Вставляем изображение
        c.drawImage(image_path, x, y, width=width, height=height, preserveAspectRatio=True, mask='auto')
        c.save()

        # Перематываем буфер памяти на начало
        packet.seek(0)

        # Читаем временный PDF файл
        overlay_reader: PdfReader = PdfReader(packet)
        overlay_page = overlay_reader.pages[0]

        # Объединяем первую страницу с наложением
        first_page.merge_page(overlay_page)

        # Создаем новый PDF файл для записи результата
        writer: PdfWriter = PdfWriter()
        writer.add_page(first_page)

        # Добавляем оставшиеся страницы
        for page in self.reader.pages[1:]:
            writer.add_page(page)

        # Сохраняем итоговый PDF файл
        try:
            with open(output_pdf_path, "wb") as f:
                writer.write(f)
        except IOError as e:
            raise IOError(f"Ошибка при сохранении PDF файла '{output_pdf_path}': {str(e)}")

        print(f"Изображение успешно вставлено в PDF и сохранено в '{output_pdf_path}'.")