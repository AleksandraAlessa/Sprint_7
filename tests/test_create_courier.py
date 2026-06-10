import pytest
import requests
import allure

@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, created_courier):
        # Фикстура уже создала курьера, проверим авторизацию (опционально)
        login_payload = {
            "login": created_courier["login"],
            "password": created_courier["password"]
        }
        login_response = requests.post(f"{created_courier['base_url']}/api/v1/courier/login", data=login_payload)
        assert login_response.status_code == 200
        assert "id" in login_response.json()

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self, base_url, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": created_courier["password"],
            "firstName": created_courier["firstName"]
        }
        response = requests.post(f"{base_url}/api/v1/courier", data=payload)
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.text

    @allure.title("Отсутствие обязательного поля (login или password)")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, base_url, courier_data, missing_field):
        payload = courier_data.copy()
        del payload[missing_field]
        response = requests.post(f"{base_url}/api/v1/courier", data=payload)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text