import flet as ft


class MainPage(ft.View):
    """
    Главная страница приложения.

    Предоставляет интерфейс для управления штрихкодами, выбора директорий с PDF-файлами,
    указания папки для сохранения обработанных файлов и запуска обработки.
    """

    def __init__(self, controller) -> None:
        """
        Инициализация главной страницы приложения.

        Args:
            controller: Контроллер главной страницы (MainPageController).
        """

        #
        super().__init__(route="/")
        self.controller = controller
        self.page = self.controller.app_controller.page

        # Инициализация данных
        self.barcodes_count = None  # Количество штрихкодов, обновляется контроллером

        # Элементы интерфейса
        self.title = ft.Text(
            "Barcode Manager",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK87
        )

        # Поле с количеством штрихкодов
        self.barcode_count_text = ft.Text(
            f"Свободные штрихкоды: {self.barcodes_count}",
            color=ft.Colors.BLACK87
        )

        # Кнопка для перехода на страницу добавления штрихкодов
        self.replenish_button = ft.ElevatedButton(
            "Добавить",
            icon=ft.Icons.ADD,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            on_click=lambda _: self.page.go("/addbarcodes")
        )

        # Поле для ввода пути к папке с PDF файлами
        self.folder_path_field = ft.TextField(
            label="Папка с PDF файлами",
            width=400,
            border_color=ft.Colors.BLUE,
            read_only=True
        )

        # Кнопка для выбора папки с PDF файлами
        self.browse_button = ft.ElevatedButton(
            "Обзор",
            icon=ft.Icons.FOLDER_OPEN,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            on_click=lambda e: None
        )

        # Поле для ввода пути к папке для сохранения готовых файлов
        self.output_folder_field = ft.TextField(
            label="Папка для сохранения готовых файлов",
            width=400,
            border_color=ft.Colors.BLUE,
            read_only=True
        )

        # Кнопка для выбора папки для сохранения готовых файлов
        self.output_browse_button = ft.ElevatedButton(
            "Обзор",
            icon=ft.Icons.FOLDER_OPEN,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            on_click=lambda e: None
        )

        # Кнопка для запуска обработки PDF файлов
        self.start_button = ft.ElevatedButton(
            "Запуск",
            icon=ft.Icons.PLAY_ARROW,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            width=200,
            height=45,
            on_click=lambda _: None
        )

        # Кнопка для перехода на страницу архива
        self.archive_button = ft.ElevatedButton(
            "Архив",
            icon=ft.Icons.ARCHIVE,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            width=200,
            height=45,
            on_click=lambda _: None
        )

        self.build_view()

    def build_view(self) -> None:
        """
        Собирает и размещает элементы интерфейса на странице.

        Создаёт контейнер с колонкой элементов, включая заголовок, текст количества штрихкодов,
        поля ввода и кнопки.
        """
        self.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        self.title,
                        ft.Divider(color=ft.Colors.BLACK26, thickness=1),
                        ft.Row(
                            [self.barcode_count_text, self.replenish_button],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [self.folder_path_field, self.browse_button],
                            spacing=10
                        ),
                        ft.Row(
                            [self.output_folder_field, self.output_browse_button],
                            spacing=10
                        ),
                        self.start_button,
                        self.archive_button
                    ],
                    spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(
                    blur_radius=8,
                    color=ft.Colors.BLACK26,
                    offset=ft.Offset(2, 2)
                )
            )
        )