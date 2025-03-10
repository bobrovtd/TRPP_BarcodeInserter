import flet as ft
from src.controller.page_controllers import MainPageController, BarcodesPageController


class MainController:
    """
    Главный контроллер приложения.

    Управляет маршрутизацией страниц, настройкой окна и взаимодействием с дочерними контроллерами.
    """
    # Константы для настроек окна
    WINDOW_WIDTH: int = 600
    WINDOW_HEIGHT: int = 400

    def __init__(self, page: ft.Page) -> None:
        """
        Инициализация главного контроллера приложения.

        Args:
            page (ft.Page): Объект страницы Flet для управления интерфейсом.
        """
        self.page: ft.Page = page

        # Настройки окна
        self.page.window.width = self.WINDOW_WIDTH
        self.page.window.height = self.WINDOW_HEIGHT
        self.page.window.resizable = False

        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # Контроллеры страниц
        self.controllers = {
            '/': MainPageController(self),
            '/addbarcodes': BarcodesPageController(self)
        }

        self.page.on_route_change = lambda e: self.route_change(e.route)
        self.page.go("/")

    def route_change(self, route: str) -> None:
        """
        Обработчик изменения маршрута.

        Очищает текущие представления и загружает соответствующую страницу по маршруту.

        Args:
            route (str): Новый маршрут страницы.
        """
        self.page.views.clear()
        controller = self.controllers.get(route)
        self.page.views.append(controller.view)
        self.page.update()
