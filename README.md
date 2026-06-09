# Sprint_7: API-тесты сервиса «Яндекс.Самокат»

## Описание
Проект содержит автоматизированные тесты для проверки API учебного сервиса [«Яндекс.Самокат»](https://qa-scooter.praktikum-services.ru/docs/).

Тесты покрывают следующие ручки:
- **Создание курьера** (`POST /api/v1/courier`)
- **Логин курьера** (`POST /api/v1/courier/login`)
- **Создание заказа** (`POST /api/v1/orders`)
- **Список заказов** (`GET /api/v1/orders`)

## Технологии
- Python 3.14
- pytest – тестовый фреймворк
- requests – отправка HTTP-запросов
- Allure – генерация отчётов
- Faker (опционально) – генерация случайных данных

## Структура проекта
Sprint_7/
├── tests/ # Все тесты
│ ├── test_create_courier.py
│ ├── test_login_courier.py
│ ├── test_create_order.py
│ └── test_orders_list.py
├── helpers/ # Вспомогательные функции
│ └── courier_helpers.py # генерация случайных строк
├── data.py # Константы (URL, данные заказа)
├── conftest.py # Фикстуры (base_url)
├── .gitignore
├── requirements.txt
└── README.md

## Установка и запуск

1. Клонирование репозитория
git clone https://github.com/AleksandraAlessa/Sprint_7.git
cd Sprint_7
2. Создание и активация виртуального окружения
bash
python -m venv .venv
source .venv/Scripts/activate   # для Windows Git Bash
# или .venv\Scripts\activate    # для Windows CMD
3. Установка зависимостей
bash
pip install -r requirements.txt
4. Запуск всех тестов
bash
pytest tests/ -v --alluredir=allure_results
5. Генерация Allure-отчёта
bash
allure serve allure_results
(требуется предварительно установить Allure commandline)

## Параметризация и генерация данных
Для создания уникальных логинов и паролей используется функция generate_random_string() из helpers/courier_helpers.py.

Для создания заказа применяется параметризация по цветам (BLACK, GREY, оба цвета, без цвета).

## Отчет о тестировании:
Из 16 тестов 14 прошли проверку Passed, 2 теста - Failed
1. Тест на отсутствие поля password при логине может возвращать 504 Gateway Timeout вместо 400 – это баг

2. Поле firstName при создании курьера упал, потому что API вернул код 201 вместо ожидаемого 400 - это баг.


# Sprint_7
# Sprint_7
# Sprint_7
