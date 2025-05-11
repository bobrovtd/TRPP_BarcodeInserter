import sys

from cx_Freeze import setup, Executable

setup(
    name="Пример Flet",
    version="1.0",
    description="Пример приложения на Flet для macOS",
    executables=[
        Executable(
            "main.py",
            target_name="ПримерFlet.app",
            base="Win32GUI" if sys.platform == "win32" else None,
        )
    ]
)



