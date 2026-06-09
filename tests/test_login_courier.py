import allure
import pytest
import requests
from helpers.courier_helpers import generate_random_string

@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера, возвращается id")
    def test_login_success(self, base_url):
        # 1. Создаём курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        create_payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        create_response = requests.post(f"{base_url}/api/v1/courier", data=create_payload)
        assert create_response.status_code == 201

        # 2. Пытаемся авторизоваться
        login_payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f"{base_url}/api/v1/courier/login", data=login_payload)
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Ошибка при авторизации: неправильный логин")
    def test_login_wrong_login(self, base_url):
        # 1. Создаём курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        create_payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        create_response = requests.post(f"{base_url}/api/v1/courier", data=create_payload)
        assert create_response.status_code == 201

        # 2. Пробуем войти с неправильным логином
        wrong_login_payload = {
            "login": login + "wrong",
            "password": password
        }
        response = requests.post(f"{base_url}/api/v1/courier/login", data=wrong_login_payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.title("Ошибка при авторизации: неправильный пароль")
    def test_login_wrong_password(self, base_url):
        # 1. Создаём курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        create_payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        create_response = requests.post(f"{base_url}/api/v1/courier", data=create_payload)
        assert create_response.status_code == 201

        # 2. Пробуем войти с неправильным паролем
        wrong_password_payload = {
            "login": login,
            "password": password + "wrong"
        }
        response = requests.post(f"{base_url}/api/v1/courier/login", data=wrong_password_payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_login_non_existent_user(self, base_url):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
        response = requests.post(f"{base_url}/api/v1/courier/login", data=payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.title("Ошибка: Недостаточно данных для входа")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, base_url, missing_field):
        # Генерируем данные, но затем удаляем одно поле
        login = generate_random_string(10)
        password = generate_random_string(10)
        payload = {"login": login, "password": password}
        del payload[missing_field]
        response = requests.post(f"{base_url}/api/v1/courier/login", data=payload)
        assert response.status_code == 400
        # Ожидаемый текст ошибки 
        assert "Недостаточно данных для входа" in response.text 