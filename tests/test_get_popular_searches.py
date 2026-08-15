from mongo_logger import get_popular_searches


def test_get_popular_searches():
    """Проверяет получение популярных поисковых запросов."""
    result = get_popular_searches()

    assert isinstance(result, list)
    assert len(result) <= 5