from pathlib import Path
from src.view.ui_notifications import show_dialog
from typing import Callable


def handle_validation_errors(func: Callable) -> Callable:
    """
    Декоратор для автоматической обработки ошибок валидации.

    Args:
        func (Callable): Функция, которую нужно обернуть.

    Returns:
        Callable: Обернутая функция с обработкой исключений.
    """

    def wrapper(controller: 'Controller', *args, **kwargs):
        try:
            return func(controller, *args, **kwargs)
        except Exception as e:
            show_dialog(controller.app_controller.page, "Ошибка", str(e))

    return wrapper


class Validator:
    """
    Класс Validator предоставляет методы для проверки и управления файлами и директориями.

    Содержит статические методы для валидации путей, типов файлов и их свойств.
    """
    SUPPORTED_IMAGE_EXTENSIONS: tuple[str, ...] = (".png", ".jpg", ".jpeg")  # Поддерживаемые расширения изображений
    EXCEL_EXTENSION: str = ".xlsx"  # Расширение Excel
    PDF_EXTENSION: str = ".pdf"  # Расширение PDF

    @staticmethod
    def is_path_exists(path: str) -> bool:
        """
        Проверяет существование пути (файла или директории).

        Args:
            path (str): Путь для проверки.

        Returns:
            bool: True, если путь существует, иначе False.
        """
        return Path(path).exists()

    @staticmethod
    def is_file_exists(file_path: str) -> bool:
        """
        Проверяет существование файла.

        Args:
            file_path (str): Путь к файлу.

        Returns:
            bool: True, если файл существует, иначе False.
        """
        path: Path = Path(file_path)
        return path.is_file()

    @staticmethod
    def is_directory_exists(dir_path: str) -> bool:
        """
        Проверяет существование директории.

        Args:
            dir_path (str): Путь к директории.

        Returns:
            bool: True, если директория существует, иначе False.
        """
        path: Path = Path(dir_path)
        return path.is_dir()

    @staticmethod
    def is_dir_empty(dir_path: str) -> bool:
        """
        Проверяет, является ли директория пустой.

        Args:
            dir_path (str): Путь к директории.

        Returns:
            bool: True, если директория пуста или не существует, иначе False.
        """
        path: Path = Path(dir_path)
        if path.is_dir():
            return not any(path.iterdir())
        return False

    @staticmethod
    def is_excel(file_path: str) -> bool:
        """
        Проверяет, является ли файл валидным Excel (.xlsx).

        Args:
            file_path (str): Путь к файлу.

        Returns:
            bool: True, если файл является .xlsx.

        Raises:
            FileNotFoundError: Если файл не существует.
            ValueError: Если файл не имеет расширения .xlsx.
        """
        path: Path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл {file_path} не найден.")
        if path.suffix != Validator.EXCEL_EXTENSION:
            raise ValueError(f"Файл {file_path} не является файлом {Validator.EXCEL_EXTENSION}.")
        return True

    @staticmethod
    def is_pdf(file_path: str) -> None:
        """
        Проверяет, является ли файл валидным PDF.

        Args:
            file_path (str): Путь к файлу.

        Raises:
            FileNotFoundError: Если файл не существует.
            ValueError: Если файл не имеет расширения .pdf.
        """
        path: Path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл {file_path} не найден.")
        if path.suffix != Validator.PDF_EXTENSION:
            raise ValueError(f"Файл {file_path} не является файлом {Validator.PDF_EXTENSION}.")

    @staticmethod
    def is_image(file_path: str) -> None:
        """
        Проверяет, является ли файл изображением.

        Args:
            file_path (str): Путь к файлу.

        Raises:
            FileNotFoundError: Если файл не существует.
            ValueError: Если файл не имеет поддерживаемого расширения изображения.
        """
        path: Path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл {file_path} не найден.")
        if path.suffix.lower() not in Validator.SUPPORTED_IMAGE_EXTENSIONS:
            raise ValueError(
                f"Файл {file_path} не является поддерживаемым изображением. "
                f"Поддерживаемые форматы: {', '.join(Validator.SUPPORTED_IMAGE_EXTENSIONS)}."
            )

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Возвращает размер файла в байтах.

        Args:
            file_path (str): Путь к файлу.

        Returns:
            int: Размер файла в байтах.

        Raises:
            FileNotFoundError: Если файл не существует.
            OSError: Если не удалось получить информацию о файле.
        """
        path: Path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        try:
            return path.stat().st_size
        except OSError as e:
            raise OSError(f"Ошибка при получении размера файла '{file_path}': {e}")