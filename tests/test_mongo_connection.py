from mongo_logger import connect


def test_mongo_connection():
    """Проверяет подключение к MongoDB."""
    with connect() as client:
        assert client is not None