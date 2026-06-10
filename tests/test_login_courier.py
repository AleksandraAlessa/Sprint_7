import allure
import pytest
import requests
from data import BASE_URL

@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера, возвращается id")
    def test_login_success(self, created_courier):
        login_payload = {
            "login": created_courier["login"],
            "password": created_courier["password"]
        }
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=login_payload)
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)
        # Дополнительно проверим, что id совпадает с id созданного курьера
        assert response.json()["id"] == created_courier["id"]

    @allure.title("Ошибка при авторизации: неправильный логин")
    def test_login_wrong_login(self, created_courier):
        wrong_login_payload = {
            "login": created_courier["login"] + "wrong",
            "password": created_courier["password"]
        }
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=wrong_login_payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.title("Ошибка при авторизации: неправильный пароль")
    def test_login_wrong_password(self, created_courier):
        wrong_password_payload = {
            "login": created_courier["login"],
            "password": created_courier["password"] + "wrong"
        }
        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=wrong_password_payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_login_non_existent_user(self, base_url, courier_data):
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        response = requests.post(f"{base_url}/api/v1/courier/login", data=payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.title("Ошибка: Недостаточно данных для входа")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, base_url, courier_data, missing_field):
        payload = courier_data.copy()
        del payload[missing_field]
        response = requests.post(f"{base_url}/api/v1/courier/login", data=payload)
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.text