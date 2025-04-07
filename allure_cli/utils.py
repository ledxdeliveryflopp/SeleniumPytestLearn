import base64
import os

from settings import cli_settings


def decode_allure_files() -> list:
    files = os.listdir(cli_settings.allure_results_dir)
    results = []
    for file in files:
        result = {}

        file_path = f"{cli_settings.allure_results_dir}{file}"
        with open(file_path, "rb") as f:
            content = f.read()
            if content.strip():
                b64_content = base64.b64encode(content)
                result['file_name'] = file
                result['content_base64'] = b64_content.decode('UTF-8')
                results.append(result)
            else:
                pass
    return results
