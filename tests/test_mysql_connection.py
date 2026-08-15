from mysql_connector import connect

def test_connection():
    """
    Тест проверяет установку соединения с базой данных

    """
    with connect() as connection:
        assert connection.is_connected()