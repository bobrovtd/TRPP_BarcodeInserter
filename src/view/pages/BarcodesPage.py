import flet as ft


class BarcodesPage(ft.View):
    """
    Страница добавления штрихкодов в базу.

    Предоставляет интерфейс для выбора файла или директории с Excel-файлами,
    содержащими штрихкоды, и запуска их обработки.
    """

    def __init__(self, controller) -> None:
        """
        Инициализация страницы добавления штрихкодов.

        Args:
            controller: Контроллер страницы (BarcodesPageController).
        """
        super().__init__(route="/addbarcodes")
        self.controller = controller

        # Заголовок страницы
        self.title = ft.Text(
            "Добавление штрихкодов в базу данных",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK87
        )

        # Кнопки выбора режима
        self.mode_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="file", label="Один файл"),
                ft.Radio(value="directory", label="Директория"),
            ]),
            value="file",
            on_change=self.on_mode_change
        )

        # Поле для пути к файлу или директории
        self.path_field = ft.TextField(
            label="Выберите файл.",
            width=400,
            height=50,
            border_color=ft.Colors.BLUE,
            read_only=True
        )

        # Кнопка "Обзор"
        self.browse_button = ft.ElevatedButton(
            "Обзор",
            icon=ft.Icons.FOLDER_OPEN,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            on_click=lambda e: None
        )

        # Кнопка "Старт"
        self.start_button = ft.ElevatedButton(
            "Старт",
            icon=ft.Icons.PLAY_ARROW,
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
            on_click=lambda _: None
        )

        # Кнопка "Назад"
        self.back_button = ft.ElevatedButton(
            "Назад",
            icon=ft.Icons.ARROW_BACK,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            on_click=lambda _: self.page.go("/")
        )

        self.build_view()

    def on_mode_change(self, e: ft.ControlEvent) -> None:
        """
        Обработчик изменения режима выбора (файл или директория).

        Args:
            e: Событие изменения значения RadioGroup.

        Raises:
            AttributeError: Если page не поддерживает метод update.
        """
        mode = self.mode_radio.value
        if mode == "file":
            self.path_field.label = "Выберите файл."
        elif mode == "directory":
            self.path_field.label = "Выберите директорию."
        self.path_field.value = ""
        try:
            self.page.update()
        except AttributeError as exc:
            raise AttributeError(f"Ошибка при обновлении страницы: {exc}")

    def build_view(self) -> None:
        """
        Собирает элементы интерфейса страницы.

        Добавляет все элементы в контейнер и настраивает их расположение.
        """
        self.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        self.title,
                        self.mode_radio,  # Горизонтальные радиокнопки
                        ft.Row([self.path_field, self.browse_button], spacing=10),
                        self.start_button,
                        self.back_button
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK26)
            )
        )