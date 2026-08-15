from mysql_connector import get_films_count_by_category_id_and_year


def test_get_films_count_by_category_id_and_year():
    """Проверяет количество фильмов по жанру и диапазону лет."""
    result = get_films_count_by_category_id_and_year(
        category_id=1,
        year_from=2005,
        year_to=2006
    )

    print(f"result = {result}")
    assert isinstance(result, int)
    assert result > 0