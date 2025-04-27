import shutil
import subprocess
from typing import List
import sys
from pathlib import Path
import os


class Utilities:
    """
    Класс для работы с файлами: удаление, перемещение, переименование.

    Содержит статические методы для управления файлами и директориями.
    """

    @staticmethod
    def move_file(source_path: str, destination_path: str) -> None:
        """
        Перемещает файл из одной директории в другую.

        Args:
            source_path (str): Путь к исходному файлу.
            destination_path (str): Путь к директории назначения или полное имя файла в этой директории.

        Raises:
            FileNotFoundError: Если исходный файл не найден.
            ValueError: Если директория назначения не существует.
            OSError: Если перемещение не удалось из-за системной ошибки.
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Файл не найден: {source_path}")

        if os.path.isdir(destination_path):
            destination_path = os.path.join(destination_path, os.path.basename(source_path))

        destination_dir: str = os.path.dirname(destination_path)
        if not os.path.exists(destination_dir):
            raise ValueError(f"Директория назначения не найдена: {destination_dir}")

        try:
            shutil.move(source_path, destination_path)
            print(f"Файл '{source_path}' перемещен в '{destination_path}'.")
        except OSError as e:
            raise OSError(f"Ошибка при перемещении файла '{source_path}' в '{destination_path}': {e}")

    @staticmethod
    def rename_file(file_path: str, new_name: str) -> None:
        """
        Переименовывает файл.

        Args:
            file_path (str): Путь к файлу, который нужно переименовать.
            new_name (str): Новое имя файла (без пути).

        Raises:
            FileNotFoundError: Если файл не найден.
            ValueError: Если новое имя некорректно.
            OSError: Если переименование не удалось из-за системной ошибки.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        if not new_name or '/' in new_name or '\\' in new_name:
            raise ValueError(f"Некорректное имя файла: {new_name}")

        directory: str = os.path.dirname(file_path)
        new_path: str = os.path.join(directory, new_name)

        try:
            os.rename(file_path, new_path)
            print(f"Файл '{file_path}' переименован в '{new_path}'.")
        except OSError as e:
            raise OSError(f"Ошибка при переименовании файла '{file_path}' в '{new_path}': {e}")

    @staticmethod
    def count_files_by_extension(dir_path: str, extension: str) -> int:
        """
        Подсчитывает количество файлов с указанным расширением в директории.

        Args:
            dir_path (str): Путь к директории.
            extension (str): Расширение файлов для подсчета (например, '.png').

        Returns:
            int: Количество файлов с указанным расширением.

        Raises:
            ValueError: Если путь не является директорией.
        """
        path: Path = Path(dir_path)
        if path.is_dir():
            return sum(1 for file in path.iterdir() if file.is_file() and file.suffix == extension)
        else:
            raise ValueError(f"Путь не является директорией: {dir_path}")

    @staticmethod
    def get_files_with_extension(dir_path: str, *extensions: str) -> List[str]:
        """
        Получает полные пути для файлов с указанным расширением.

        Args:
            dir_path (str): Путь к директории.
            *extensions (str): Расширения файлов для поиска (например, '.png', '.jpg').

        Returns:
            List[str]: Список полных путей к файлам с указанными расширениями.

        Raises:
            ValueError: Если путь не является директорией.
        """
        path: Path = Path(dir_path)
        if path.is_dir():
            return [str(file) for file in path.iterdir() if file.is_file() and file.suffix.lower() in extensions]
        else:
            raise ValueError(f"Путь не является директорией: {dir_path}")

    @staticmethod
    def create_directory(*dir_path: str) -> None:
        """
        Создает директорию, если она не существует.

        Args:
            *dir_path (str): Пути к создаваемым директориям.

        Raises:
            OSError: Если создание директории не удалось из-за системной ошибки.
        """
        for path in dir_path:
            path_obj: Path = Path(path)
            if not path_obj.exists():
                try:
                    path_obj.mkdir(parents=True, exist_ok=True)
                except OSError as e:
                    raise OSError(f"Ошибка при создании директории '{path}': {e}")

    @staticmethod
    def delete_file(file_path: str) -> None:
        """
        Удаляет файл.

        Args:
            file_path (str): Путь к удаляемому файлу.

        Raises:
            FileNotFoundError: Если файл не найден.
            OSError: Если удаление не удалось из-за системной ошибки.
        """
        path: Path = Path(file_path)
        if path.is_file():
            try:
                path.unlink()
            except OSError as e:
                raise OSError(f"Ошибка при удалении файла '{file_path}': {e}")
        else:
            raise FileNotFoundError(f"Файл не найден: {file_path}")

    @staticmethod
    def delete_directory(dir_path: str, force: bool = False) -> None:
        """
        Удаляет директорию.

        Args:
            dir_path (str): Путь к удаляемой директории.
            force (bool, optional): Если True, удаляет директорию со всем содержимым. По умолчанию False.

        Raises:
            FileNotFoundError: Если директория не найдена.
            OSError: Если удаление не удалось из-за системной ошибки или директория не пуста (при force=False).
        """
        path: Path = Path(dir_path)
        if path.is_dir():
            try:
                if force:
                    shutil.rmtree(dir_path)
                else:
                    path.rmdir()
            except OSError as e:
                raise OSError(f"Ошибка при удалении директории '{dir_path}': {e}")
        else:
            raise FileNotFoundError(f"Директория не найдена: {dir_path}")

    @staticmethod
    def open_folder(path: str) -> None:
        """
        Открывает папку в ОС по указанному пути.

        Args:
            path (str): Путь к открываемой папке.

        Raises:
            ValueError: Если путь не является директорией или не существует.
        """
        path_obj: Path = Path(path)

        if not path_obj.exists():
            # Создаем директорию, если она не существует
            try:
                os.makedirs(path_obj)
            except Exception as ex:
                raise ValueError(f"Не удалось создать папку {path}: {ex}")
        elif not path_obj.is_dir():
            raise ValueError(f"Путь {path} не является папкой!")

        # Открываем папку
        try:
            if sys.platform == 'win32':  # Windows
                os.startfile(str(path_obj))
            elif sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', str(path_obj)])
            else:  # Linux и другие UNIX-системы
                subprocess.Popen(['xdg-open', str(path_obj)])
        except Exception as ex:
            print(f"Ошибка открытия папки {path}: {ex}")
