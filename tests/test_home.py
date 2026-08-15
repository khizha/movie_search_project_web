from app import app
# Из файла app.py импортируем объект Flask с именем app


def test_home():
    """Проверяет открытие главной страницы."""
    client = app.test_client() # тестовый клиент Flask
    response = client.get("/") # имитация открытия адреса "/"
    assert response.status_code == 200