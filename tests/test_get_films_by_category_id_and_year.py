from mysql_connector import get_films_by_category_id_and_year


def test_get_films_by_category_id_and_year():
    """Проверяет поиск фильмов по жанру и диапазону лет."""
    result = get_films_by_category_id_and_year(
        category_id=1,
        year_from=2005,
        year_to=2006,
        limit=10,
        offset=0
    )

    assert isinstance(result, list)
    assert len(result) <= 10