from faker import Faker
import json
import requests
from data import BASE_URL
import random
import string

# Инициализируем Faker с русской локализацией
fake = Faker('ru_RU')

def generate_random_string_custom(length=10):
    """Генерирует заданное количество случайных символов (на случай, если Faker не подходит)."""
    return fake.bothify(text='?'*length) # Заменит ? на случайную букву или цифру

def register_new_courier_and_return_login_password():
    """Генерирует данные и создаёт нового курьера через API."""
    # Генерируем реалистичные, но случайные данные
    login = fake.user_name()               # Логин вида 'ivanov_ivan'
    password = fake.password(length=10)    # Пароль из 10 символов
    first_name = fake.first_name()         # Имя 'Иван'

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

    if response.status_code == 201:
        # Если успех, возвращаем логин и пароль для последующих тестов
        return login, password, first_name
    return None, None, None

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))