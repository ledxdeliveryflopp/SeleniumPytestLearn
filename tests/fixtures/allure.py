import os
import shutil

import allure
import pytest


def clear_allure_static_folder() -> None:
    try:
        files = os.listdir("./allure_static/")
        for file in files:
            os.remove(f"./allure_static/{file}")
    except Exception as exc:
        print(exc)


@pytest.fixture(scope="session", autouse=True)
@allure.title("Очистка директории скриншотов Selenium")
def clear_static_folder() -> None:
    clear_allure_static_folder()
    yield
    clear_allure_static_folder()


@pytest.fixture(scope="session", autouse=True)
@allure.title("Копирование environment.properties в allure-results")
def add_env_file_in_allure() -> None:
    shutil.copyfile("tests/environment.properties", "./allure-results/environment.properties")
