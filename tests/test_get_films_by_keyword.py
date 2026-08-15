from mysql_connector import get_films_by_keyword


def test_get_films_by_keyword():
    """
    Проверяет работу функции поиска фильмов
    по ключевому слову.
    :result список из первых не более 10 найденных
    фильмов
    """
    result = get_films_by_keyword("ant", 10, 0)

    assert isinstance(result, list)
    assert len(result) <= 10