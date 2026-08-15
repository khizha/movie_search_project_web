from mysql_connector import get_films_count_by_keyword


def test_get_films_count_by_keyword():
    """Проверяет количество фильмов, найденных по ключевому слову."""
    result = get_films_count_by_keyword("ant")
    print(f"result = {result}")

    assert isinstance(result, int)
    assert result > 0