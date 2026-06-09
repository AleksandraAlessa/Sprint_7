import pytest
from helpers.courier_helpers import register_new_courier_and_return_login_password
import requests
from helpers.courier_helpers import generate_random_string
import allure

@allure.feature("Создание курьера")
class TestCreateCourier:
    # 1. Проверка успешного создания курьера
    @allure.title("Успешное создание курьера")
    @allure.step("Отправить POST-запрос на создание курьера")
    def test_create_courier_success(self, base_url):
        with allure.step("Генерируем уникальные данные для курьера"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }

        with allure.step(f"Отправить запрос на создание курьера с логином {login}"):
            response = requests.post(f"{base_url}/api/v1/courier", data=payload)
            
        with allure.step("Проверить код ответа 201 и тело {ok: true}"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

    # 2. Проверка, что нельзя создать двух одинаковых курьеров
    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.step("Создать курьера с уникальными данными и повторить запрос")
    def test_cannot_create_duplicate_courier(self, base_url):
        # генерируем уникальные данные
        with allure.step("Генерируем данные курьера"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
        with allure.step("Первый запрос – создание курьера"):
        # создаём курьера первый раз – должно быть успешно
            response1 = requests.post(f"{base_url}/api/v1/courier", data=payload)
            assert response1.status_code == 201

        with allure.step("Второй запрос с теми же данными – ожидаем конфликт"):
        # создаём такого же курьера второй раз – должна быть ошибка 409
            response2 = requests.post(f"{base_url}/api/v1/courier", data=payload)
            assert response2.status_code == 409
        # проверяем текст ошибки 
            assert "Этот логин уже используется" in response2.text
    
    # 3. Тест на проверку отсутсвия каждого из обязательных полей
    @allure.title("Отсутствие одного из обязательных полей")
    @allure.step("Проверка ошибки при отсутствии поля {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"]) # запускает один и тот же тест три раза: с отсутствующим полем login, затем password, затем firstName
    def test_create_courier_missing_field(self, base_url, missing_field):
        with allure.step(f"Генерируем данные, удаляем поле {missing_field}"):
        # генерируем данные для всех полей
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
        # удаляем одно из обязательных полей
        del payload[missing_field]
        
        with allure.step("Отправить запрос с неполными данными"):
            response = requests.post(f"{base_url}/api/v1/courier", data=payload)
        
        with allure.step("Проверить код 400 и сообщение об ошибке"):
            assert response.status_code == 400
        # проверяем сообщение об ошибке (может быть "Недостаточно данных" или похожее)
            assert "Недостаточно данных для создания учетной записи" in response.text 