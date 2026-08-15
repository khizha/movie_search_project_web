from mongo_logger import get_recent_searches


def test_get_recent_searches():
    """Проверяет получение последних поисковых запросов."""
    result = get_recent_searches()

    assert isinstance(result, list)
    assert len(result) <= 5