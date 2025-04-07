import json

import allure
import pytest
from selenium import webdriver

from consts.drivers import drivers_const


class DriverService:
    selenoid: bool
    driver: str
    lang: str

    def __init__(self):
        self.__init_driver_settings()

    def __init_driver_settings(self) -> None:
        """Инициализация настроек Selenium"""
        try:
            with open("tests/settings.json") as file:
                data: dict = json.load(file)
            self.selenoid = data.get("selenoid_run")
            driver = data.get("selenium_driver")
            self.lang = data.get("browser_lang")
            selenium_driver: str = drivers_const.browser_drivers.drivers.get(driver)
            self.driver = selenium_driver
        except Exception as exc:
            raise Exception(f"Ошибка при установке драйвера Selenium: {exc}")

    def init_selenium_driver(self) -> webdriver.Remote:
        """Инициализация драйвера Selenium"""
        driver_options = getattr(webdriver, self.driver)()
        if self.selenoid is True:
            driver_options.set_capability("selenoid:options", {"enableVNC": True})
            driver_options.add_argument(f"--lang={self.lang}")
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                options=driver_options)
            return driver
        driver_options.add_argument(f"--lang={self.lang}")
        driver = webdriver.Chrome(options=driver_options)
        return driver


driver_service = DriverService()


@pytest.fixture
@allure.title("Установка драйвера для Selenium")
def driver():
    selenium_driver = driver_service.init_selenium_driver()
    selenium_driver.implicitly_wait(10)
    selenium_driver.maximize_window()
    yield selenium_driver
    selenium_driver.quit()


@pytest.fixture
@allure.title("Установка настроек браузера")
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium
