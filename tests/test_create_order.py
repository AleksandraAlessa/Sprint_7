import allure
import pytest
import requests
from data import BASE_URL, DEFAULT_ORDER_DATA

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        # Копируем базовые данные и добавляем/переопределяем цвет
        payload = DEFAULT_ORDER_DATA.copy()
        payload["color"] = color

        response = requests.post(f"{BASE_URL}/api/v1/orders", json=payload)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)