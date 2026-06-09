import allure
import requests
from data import BASE_URL

@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("Проверка, что тело ответа содержит список заказов")
    def test_orders_list_returns_list(self):
        response = requests.get(f"{BASE_URL}/api/v1/orders")
        assert response.status_code == 200
        # Проверяем, что в ответе есть ключ 'orders'
        assert "orders" in response.json()
        # Проверяем, что значение по ключу 'orders' является списком
        assert isinstance(response.json()["orders"], list)