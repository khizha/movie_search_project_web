from app import app
# Из файла app.py импортируем объект Flask с именем app


def test_genre_invalid_years():
    """Проверяет обработку неправильного диапазона лет."""
    client = app.test_client()

    response = client.post(
        "/genre",
        data={
            "category_id": "1",
            "year_from": "2000",
            "year_to": "1990",
        }
    )

    assert response.status_code == 200
    assert "Начальный год не может быть больше конечного" in response.text