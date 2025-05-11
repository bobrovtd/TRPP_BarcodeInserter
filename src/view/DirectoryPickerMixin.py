import flet as ft


class PickerService:
    """
    Сервис для выбора файлов и директорий с использованием FilePicker из Flet.

    Управляет одним экземпляром FilePicker, обрабатывает выбор файлов и директорий,
    обновляет целевые виджеты и вызывает функции обратного вызова.
    """

    def __init__(self, page: ft.Page) -> None:
        """
        Инициализация сервиса выбора файлов и директорий.

        Args:
            page: Объект страницы Flet для управления интерфейсом.
        """
        self.page = page
        # Создаём один FilePicker для всех операций
        self.file_picker = ft.FilePicker(on_result=self._on_picker_result)
        self.page.overlay.append(self.file_picker)
        self._current_callback = None  # Может быть None или функцией, принимающей str
        self._current_target = None  # Может быть None или виджетом ft.Control

    def pick_directory(self, target_widget=None, callback=None) -> None:
        """
        Открывает диалог для выбора директории.

        Args:
            target_widget: Виджет, в который будет записан путь (может быть None).
            callback: Функция обратного вызова, принимающая путь (может быть None).
        """
        self._current_target = target_widget
        self._current_callback = callback
        self.file_picker.get_directory_path()

    def pick_file(self, target_widget=None, callback=None, file_type=None) -> None:
        """
        Открывает диалог для выбора файла.

        Args:
            target_widget: Виджет, в который будет записан путь (может быть None).
            callback: Функция обратного вызова, принимающая путь (может быть None).
            file_type: Тип файла для фильтрации (например, 'image', 'pdf'), по умолчанию None.
        """
        self._current_target = target_widget
        self._current_callback = callback
        self.file_picker.pick_files(allow_multiple=False, file_type=file_type)

    def _on_picker_result(self, e: ft.FilePickerResultEvent) -> None:
        """
        Обрабатывает результат выбора файла или директории.

        Args:
            e: Событие результата выбора от FilePicker.

        Raises:
            AttributeError: Если целевой виджет не поддерживает атрибут value или update.
        """
        target_widget = self._current_target
        callback = self._current_callback
        # Получаем путь: для директории — e.path, для файла — e.files[0].path
        path = e.path if e.path else (e.files[0].path if e.files else None)

        # Если указан виджет, обновляем его значение
        if path and target_widget:
            try:
                target_widget.value = path
                target_widget.update()
            except AttributeError as exc:
                raise AttributeError(f"Целевой виджет не поддерживает обновление значения: {exc}")

        # Если указан callback, вызываем его с путём
        if callback and path:
            callback(path)

        # Очищаем временные переменные
        self._current_callback = None
        self._current_target = None
