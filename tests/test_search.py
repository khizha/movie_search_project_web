from app import app
# Из файла app.py импортируем объект Flask с именем app

def test_search_page():
    """Проверяет открытие страницы поиска."""
    client = app.test_client()
    response = client.get("/search")
    assert response.status_code == 200