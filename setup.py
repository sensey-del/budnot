from setuptools import setup, find_packages

setup(
    name="budNOT",
    version="0.1",
    packages=find_packages(),  # Автоматически находит все пакеты
    entry_points={
        "console_scripts": [
            "budnot=budNOT.main:main",  # Указываем полный путь к модулю
        ],
    },
    install_requires=[
        "rich",
        "questionary",
    ],
)
