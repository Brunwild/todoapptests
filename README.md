# Автоматизированное тестирование Todo App

Проект представляет собой набор автотестов для Angular-приложения "Todo List".

## Технологии

- **Python 3.11**
- **Playwright** — для автоматизации браузера
- **pytest + pytest-asyncio** — фреймворк тестирования
- **Page Object Pattern** — архитектурный подход
- **Allure** — генерация красивых отчётов

## Особенности проекта

- Стабильная работа с асинхронным API (JSONPlaceholder)
- Мокирование запросов (обход проблем с 500 ошибками сервера)
- Автоматическое создание тестовых данных
- Скриншоты при падении тестов
- Allure-отчёты с подробной визуализацией

## Структура проекта

```plaintext
todoapptests/                  # Корень проекта
├── docs/                      # Документация
│   ├── BUG_REPORTS.md
│   └── TEST_CASES.md
├── tests/                     # Все автотесты
│   ├── pages/                 # Page Objects
│   ├── test_edge_cases.py
│   └── test_todo_functionality.py
├── reports/                   # Отчёты (будет создаваться автоматически)
│   ├── allure-report/
│   └── allure-results/
├── .gitignore
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Список реализованных тестов
1. Покрыты CRUD операции (Create, Read, Update, Delete)
2. Учтены edge-cases JSONPlaceholder (успешные “фейковые” PUT/DELETE)
3. Проверены фильтры и UI состояния
4. Учтена отсутствие персистентности данных
5. Проверены race conditions из-за задержки API

## Инструкция по запуску
1. Скачать проект
2. Установить зависимости pip install -r requirements.txt
3. playwright install chromium
4. cd todoapptests\tests
5. pytest tests/ -v --html=reports/report.html --self-contained-html \\ Запустить тесты с сохранением результатов
6. allure generate reports/allure-results -o reports/allure-report --clean \\ Сгенерировать отчёт
7. allure open reports/allure-report \\ Открыть отчёт(не всегда работает, отчет генерируется в todoapptests\tests\reports\report.html)

### Параллельный запуск (по браузерам в разных процессах):
pytest -n 3 tests/ --asyncio-mode=auto
