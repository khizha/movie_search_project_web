from app import app
# Из файла app.py импортируем объект Flask с именем app


def test_genre_page():
    """Проверяет открытие страницы поиска по жанру."""
    client = app.test_client()

    response = client.get("/genre")

    assert response.status_code == 200