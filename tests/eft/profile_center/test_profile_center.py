import time

import allure
import pytest

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from eft.profile_center.const import profile_center_const


@pytest.mark.profile_center
@allure.feature("Тестирование аккаунт центра")
class TestProfileCenter:
    web_url: str = "https://profile.tarkov.com/login"

    @staticmethod
    @pytest.mark.skip(reason="Функция для сохранения скриншотов")
    def save_page_screenshot(selenium_driver: WebDriver, png_name: str, allure_name: str) -> None:
        selenium_driver.save_screenshot(f"./allure_static/{png_name}.png")
        allure.attach.file(f"./allure_static/{png_name}.png", name=allure_name,
                           attachment_type=allure.attachment_type.PNG)

    @allure.title("Проверка авторизации с пустыми обязательными полями.")
    @allure.tag("Authentication", "Profile", "Profile Center")
    @allure.link(web_url, name="eft website")
    @allure.testcase("TMS-1")
    @allure.parent_suite("Формы")
    @allure.suite("Валидация")
    @allure.sub_suite("Авторизация - пустая форма")
    def test_authorization_with_empty_form(self, selenium: WebDriver) -> None:
        with allure.step("Открытие страницы авторизации"):
            selenium.get(self.web_url)
            time.sleep(10)
            self.save_page_screenshot(selenium, f"login_page_{self.test_authorization_with_empty_form.__name__}",
                                      "Страница авторизации")
            assert profile_center_const.pages.names.get("login_page") == selenium.title
        with allure.step("Поиск элементов формы"):
            selenium.implicitly_wait(10)
            email_input = selenium.find_element(By.ID, "email")
            password_input = selenium.find_element(By.ID, "password")
        with allure.step("Отчиска формы логина"):
            email_input.clear()
            password_input.clear()
            self.save_page_screenshot(selenium, f"login_empty_page_screenshot_{self.test_authorization_with_empty_form.__name__}",
                                      "Страница авторизации с пустой формой")
        with allure.step("Отправка формы логина"):
            button = selenium.find_element(By.CLASS_NAME, "bsg-ac-form-button__name")
            button.click()
            time.sleep(5)
        with allure.step("Проверка что появилась ошибка пустой формы"):
            selenium.implicitly_wait(10)
            elems = selenium.find_elements(By.CLASS_NAME, "bsg-ac-form-input-errors")
            for elem in elems:
                if elem.text in profile_center_const.forms_texts.texts:
                    pass
            self.save_page_screenshot(selenium, f"form_errors_{self.test_authorization_with_empty_form.__name__}",
                                      "Форма с ошибками")

    @allure.title("Проверка авторизации с правильной информацией")
    @allure.tag("Authentication", "Profile", "Profile Center")
    @allure.link(web_url, name="eft website")
    @allure.testcase("TMS-1")
    @allure.parent_suite("Формы")
    @allure.suite("Валидация")
    @allure.sub_suite("Авторизация - форма с валидной информацией")
    def test_authorization_with_valid_info(self, selenium: WebDriver) -> None:
        with allure.step("Открытие страницы авторизации"):
            selenium.get(self.web_url)
            time.sleep(10)
            self.save_page_screenshot(selenium, f"login_page_{self.test_authorization_with_valid_info.__name__}",
                                      "Страница авторизации")
            assert profile_center_const.pages.names.get("login_page") == selenium.title
        with allure.step("Поиск полей формы"):
            selenium.implicitly_wait(10)
            email_input = selenium.find_element(By.ID, "email")
            password_input = selenium.find_element(By.ID, "password")
        with allure.step("Заполнение полей формы"):
            email_input.send_keys("korstim18@gmail.com")
            password_input.send_keys("AJCDEDWR1v")
            self.save_page_screenshot(selenium,
                                      f"login_fill_page_screenshot_{self.test_authorization_with_valid_info.__name__}",
                                      "Страница авторизации с заполненной формой")
        with allure.step("Отправка формы логина"):
            button = selenium.find_element(By.CLASS_NAME, "bsg-ac-form-button__name")
            button.click()
            time.sleep(5)
        with allure.step("Проверка что запрашивает код подтверждения"):
            assert profile_center_const.pages.names.get("confirm_page") == selenium.title
            self.save_page_screenshot(selenium,
                                      f"confirm_page_screenshot_{self.test_authorization_with_valid_info.__name__}",
                                      "Страница авторизации с заполненной формой")

    @allure.title("Проверка авторизации с невалидным Email")
    @allure.tag("Authentication", "Profile", "Profile Center")
    @allure.link(web_url, name="eft website")
    @allure.testcase("TMS-1")
    @allure.parent_suite("Формы")
    @allure.suite("Валидация")
    @allure.sub_suite("Авторизация - форма с невалидным Email")
    def test_authorization_with_non_valid_email(self, selenium: WebDriver) -> None:
        with allure.step("Открытие страницы авторизации"):
            selenium.get(self.web_url)
            time.sleep(10)
            self.save_page_screenshot(selenium, f"login_page_{self.test_authorization_with_non_valid_email.__name__}",
                                      "Страница авторизации")
            assert profile_center_const.pages.names.get("login_page") == selenium.title
        with allure.step("Поиск полей формы"):
            selenium.implicitly_wait(10)
            email_input = selenium.find_element(By.ID, "email")
            password_input = selenium.find_element(By.ID, "password")
        with allure.step("Заполнение полей формы"):
            email_input.send_keys("№;46")
            password_input.send_keys("test")
        self.save_page_screenshot(selenium,
                                  f"login_fill_page_screenshot_{self.test_authorization_with_non_valid_email.__name__}",
                                  "Страница авторизации с заполненной формой")
        with allure.step("Отправка формы логина"):
            button = selenium.find_element(By.CLASS_NAME, "bsg-ac-form-button__name")
            button.click()
            time.sleep(5)
        with allure.step("Поиск текста ошибки"):
            error_div = selenium.find_element(By.CLASS_NAME, "bsg-ac-form-input-errors__error")
            assert error_div.text == "Некорректный E-mail"
            self.save_page_screenshot(selenium,
                                      f"form_errors_{self.test_authorization_with_non_valid_email.__name__}",
                                      "Форма с ошибками")
