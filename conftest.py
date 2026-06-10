import pytest
from data import BASE_URL
from helpers.courier_helpers import generate_random_string
import requests

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def courier_data():
    """Генерирует уникальные данные для курьера без создания."""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }

@pytest.fixture
def created_courier(base_url, courier_data):
    """Создаёт курьера, возвращает его данные и ID, после теста удаляет."""
    payload = courier_data.copy()
    create_response = requests.post(f"{base_url}/api/v1/courier", data=payload)
    assert create_response.status_code == 201, f"Не удалось создать курьера: {create_response.text}"
    assert create_response.json() == {"ok": True}

    # Получение ID
    login_payload = {"login": payload["login"], "password": payload["password"]}
    login_response = requests.post(f"{base_url}/api/v1/courier/login", data=login_payload)
    assert login_response.status_code == 200, "Не удалось получить ID курьера"
    courier_id = login_response.json()["id"]

    # Возвращаем данные и ID
    yield {
        "login": payload["login"],
        "password": payload["password"],
        "firstName": payload["firstName"],
        "id": courier_id,
        "base_url": base_url
    }

    # Удаление
    delete_response = requests.delete(f"{base_url}/api/v1/courier/{courier_id}")
    assert delete_response.status_code == 200, f"Не удалось удалить курьера {courier_id}"