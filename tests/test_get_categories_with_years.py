from mysql_connector import get_categories_with_years


def test_get_categories_with_years():
    """Проверяет получение списка всех жанров из базы данных."""
    result = get_categories_with_years()

    assert isinstance(result, list)
    assert len(result) > 0