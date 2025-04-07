import json


class CLISettings:
    """Настройки приложения"""
    allure_results_dir: str
    allure_docker_address: str
    auto_create_project: bool

    def set_settings(self) -> None:
        try:
            with open("settings.json") as file:
                data: dict = json.load(file)
            self.allure_results_dir = data.get("allure_results")
            self.allure_docker_address = data.get("allure_docker_addr")
            self.auto_create_project = data.get("create_project_if_dont_exist")
            print(f"Директория Allure: {self.allure_results_dir}")
            print(f"Адрес Allure: {self.allure_docker_address}")
            print(f"Автоматическое создание проектов: {"Включено" if self.auto_create_project is True else "Отключено"}")
        except Exception as exc:
            raise Exception(f"Ошибка при установе настроек: {exc}")


def init_settings() -> CLISettings:
    settings = CLISettings()
    settings.set_settings()
    return settings


cli_settings = init_settings()
