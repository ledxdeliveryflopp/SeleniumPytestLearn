import argparse
import json
import time

import requests

from conts import executors_const
from settings import cli_settings
from utils import decode_allure_files


class CLIService:
    """Сервис CLI"""

    @staticmethod
    def get_parser_data(info) -> argparse.Namespace:
        """Возврат аргументов из командной строки"""
        parser = argparse.ArgumentParser(description="CLI-приложение для создания отчетов в Allure",
                                         usage="--project 1 --type ""github"" --build_name ""Git"" --build_url ""https://allurereport.org/docs/how-it-works-executor-file/")
        parser.add_argument("--project", required=True, type=str, help="Название проекта в Allure")
        parser.add_argument("--type", required=True, type=str,
                            help="Исполнитель проекта в Allure(github, gitlab и тд)")
        parser.add_argument("--build_name", required=True, type=str,
                            help="Название CI которое создавало отчет")
        parser.add_argument("--build_url", required=True, type=str or None, help="Ссылка на CI сборку")
        args = parser.parse_args(info)
        if not executors_const.executor_type.types.get(args.type):
            print(f"Неизвестный исполнитель: {args.type}")
            print(f"Список исполнителей: {[i for i in executors_const.executor_type.types]}")
            exit()
        return args

    @staticmethod
    def create_allure_project(project: str) -> None:
        """Загрузка проекта в Allure"""
        print(f"------------------СОЗДАНИЕ-ПРОЕКТА-{project.upper()}------------------")
        request_url = f"{cli_settings.allure_docker_address}/allure-docker-service/projects"
        request_body = {
            "id": project.lower()
        }
        response = requests.post(request_url, headers={'Content-type': 'application/json'},
                                 data=json.dumps(request_body), verify=True)
        if response.status_code == 201:
            print("------------------ПРОЕКТ-СОЗДАН-УСПЕШНО-ПОВТОРИТЕ-ЗАПУСК-ПРИЛОЖЕНИЯ------------------")
            exit()
        print("------------------ОШИБКА-ПРИ-СОЗДАНИИ-ПРОЕКТА------------------")
        print("КОД ОТВЕТА:")
        print(response.status_code)
        print("JSON ОТВЕТА:")
        json_response_body = json.loads(response.content)
        json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
        print(json_prettier_response_body)
        exit()

    def upload_in_allure(self, project: str) -> None:
        """Загрузка отчета в Allure"""
        results = decode_allure_files()
        request_body = {
            "results": results
        }
        print("------------------ОТПРАВКА-ОТЧЕТА------------------")
        time.sleep(5)
        request_url = f"{cli_settings.allure_docker_address}/allure-docker-service/send-results?project_id={project.lower()}"
        response = requests.post(request_url, headers={'Content-type': 'application/json'},
                                 data=json.dumps(request_body), verify=True)
        if response.status_code == 200:
            print("------------------ОТЧЕТ-ОТПРАВЛЕН-УСПЕШНО------------------")
            return
        if cli_settings.auto_create_project is True and response.status_code == 404:
            self.create_allure_project(project)
        print("------------------ОШИБКА-ПРИ-ОТПРАВКЕ-РЕЗУЛЬТАТОВ------------------")
        print("КОД ОТВЕТА:")
        print(response.status_code)
        print("JSON ОТВЕТА:")
        json_response_body = json.loads(response.content)
        json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
        print(json_prettier_response_body)
        exit()

    @staticmethod
    def do_build_report(project: str, executor: str, executor_url: str | None, execution_type: str | None) -> None:
        """Формирование отчета в Allure"""
        print("------------------ФОРМИРОВАНИЕ-ОТЧЕТА------------------")
        time.sleep(5)
        request_url = (
            f"{cli_settings.allure_docker_address}/allure-docker-service/generate-report?project_id={project.lower()}"
            f"&execution_name={executor}&execution_from={executor_url}&execution_type={execution_type}")
        response = requests.get(request_url, headers={'Content-type': 'application/json'}, verify=True)
        if response.status_code == 200:
            print("------------------ОТЧЕТ-СФОРМИРОВАН-УСПЕШНО------------------")
            json_response_body = json.loads(response.content)
            print('ССЫЛКА НА ОТЧЕТ:')
            print(json_response_body['data']['report_url'])
            return
        print("------------------ОШИБКА-ПРИ-ФОРМИРОВАНИИ-ОТЧЕТА------------------")
        print("КОД ОТВЕТА:")
        print(response.status_code)
        print("JSON ОТВЕТА:")
        json_response_body = json.loads(response.content)
        json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
        print(json_prettier_response_body)
        exit()
