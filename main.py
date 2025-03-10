from src.controller.MainController import MainController
import flet as ft


def main(page: ft.Page):
    MainController(page)


if __name__ == '__main__':
    ft.app(target=main)
