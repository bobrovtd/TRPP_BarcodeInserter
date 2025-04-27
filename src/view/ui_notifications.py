import flet as ft


def show_dialog(page: ft.Page, title: str, content: str) -> None:
    """
    Отображает статическое модальное окно (диалог) на странице Flet.

    Args:
        page: Объект страницы Flet, на которой будет отображён диалог.
        title: Заголовок диалога.
        content: Содержимое диалога.

    Raises:
        AttributeError: Если page не поддерживает атрибуты dialog или update.
    """
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[ft.TextButton("OK", on_click=lambda _: page.close_dialog())]
    )
    try:
        page.dialog = dialog
        dialog.open = True
        page.update()
    except AttributeError as e:
        raise AttributeError(f"Ошибка при отображении диалога: {e}")


def show_loading_dialog(page: ft.Page, message: str = "Обработка...") -> ft.AlertDialog:
    """
    Отображает диалог с анимацией загрузки.

    Args:
        page: Объект страницы Flet, на которой будет отображён диалог.
        message: Текст, отображаемый рядом с анимацией (по умолчанию "Обработка...").

    Returns:
        ft.AlertDialog: Созданный диалог, чтобы его можно было закрыть позже.

    Raises:
        AttributeError: Если page не поддерживает атрибуты dialog или update.
    """
    loading_dialog = ft.AlertDialog(
        title=ft.Text("Пожалуйста, подождите"),
        content=ft.Row([
            ft.ProgressRing(width=30, height=30, stroke_width=3),
            ft.Text(message)
        ]),
        modal=True  # Делаем диалог модальным, чтобы блокировать UI
    )
    try:
        page.dialog = loading_dialog
        loading_dialog.open = True
        page.update()
        return loading_dialog
    except AttributeError as e:
        raise AttributeError(f"Ошибка при отображении диалога загрузки: {e}")


def close_loading_dialog(page: ft.Page, dialog: ft.AlertDialog) -> None:
    """
    Закрывает диалог с анимацией загрузки.

    Args:
        page: Объект страницы Flet.
        dialog: Диалог, который нужно закрыть.

    Raises:
        AttributeError: Если page не поддерживает метод close_dialog.
    """
    try:
        page.close_dialog()
        page.update()
    except AttributeError as e:
        raise AttributeError(f"Ошибка при закрытии диалога загрузки: {e}")
