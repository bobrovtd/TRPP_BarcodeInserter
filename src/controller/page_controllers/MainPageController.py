from src.view.pages.MainPage import MainPage


class MainPageController:
    """
    Контроллер главной страницы приложения.

    Управляет взаимодействием с главной страницей, выбором директорий и обработкой PDF файлов со штрихкодами.
    """

    def __init__(self, app_controller: 'MainController') -> None:
        """
        Инициализация контроллера главной страницы.

        Args:
            app_controller (MainController): Главный контроллер приложения.
        """
        self.app_controller: 'MainController' = app_controller
        self.view: MainPage = MainPage(self)
        self.barcodes_count: int = -1
