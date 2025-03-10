import os

from src.view.BarcodesPage import BarcodesPage


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
        self.view = BarcodesPage(self)
        self.view.barcodes_count = 0
