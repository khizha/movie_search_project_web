from app import app
# Из файла app.py импортируем объект Flask с именем app


def test_search_empty_keyword():
    """Проверяет обработку пустого ключевого слова."""
    client = app.test_client()

    response = client.post(
        "/search",
        data={"keyword": "   "}
    )

    assert response.status_code == 200
    assert "Ключевое слово не может быть пустым" in response.text