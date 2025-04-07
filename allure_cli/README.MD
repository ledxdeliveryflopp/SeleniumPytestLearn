# Allure CLI
CLI приложения для создания отчетов Allure в docker контейнере

# Функции

1. Создание проекта Allure
2. Загрузка отчета за последний тест
3. Формирование отчета за последний тест

# Как использовать

1. Запустите скрипт
```bash
python main.py --project "my_project" --type "github" --build_name "user" --build_url "https://github.com/ledxdeliveryflopp"
```

2. Если при попытке отправить отчет будет не найден нужный проект, то:
    - Будет создан проект с нужным названием
    - Приложение сообщит об ошибке

3. При успешной отправке и формировании отчета приложение напишет url где находится отчет
```http
http://localhost:5050/allure-docker-service/projects/my_project/reports/latest/index.html
```

# Настройки

###
```json
{
  "allure_results": "../allure-results/",
  "allure_docker_addr": "http://localhost:5050",
  "create_project_if_dont_exist": true
}
```
- allure_results - Папка куда сохраняются файлы отчета Allure при тесте
- allure_docker_addr - Адрес Docker контейнера где находится Allure
- create_project_if_dont_exist - Создавать ли проект Allure если его не существует
