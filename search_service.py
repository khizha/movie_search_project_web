from mysql_connector import (
    get_films_by_keyword,
    get_categories_with_years,
    get_films_by_category_id_and_year,
    get_films_count_by_category_id_and_year,
    get_films_count_by_keyword,
)


def search_by_keyword(keyword, limit, offset) -> list[dict]:
    """
    Выполняет поиск фильмов по ключевому слову
    с постраничным выводом результатов.

    :param keyword: Ключевое слово для поиска.
    :param limit: Количество фильмов на странице.
    :param offset: Количество пропускаемых фильмов.
    :return: Список найденных фильмов.
    """
    return get_films_by_keyword(keyword, limit, offset)


def get_keyword_films_count(keyword) -> int:
    """
    Возвращает количество фильмов,
    найденных по ключевому слову.
    """
    return get_films_count_by_keyword(keyword)


def get_categories() -> list[dict]:
    """
    Возвращает список жанров с диапазоном доступных годов.

    :return: Список жанров.
    """
    return get_categories_with_years()


def search_by_category(
        category_id,
        year_from,
        year_to,
        limit,
        offset
) -> list[dict]:
    """
    Выполняет поиск фильмов по жанру и диапазону годов.

    Результат ограничен указанным количеством фильмов
    и начинается с указанной позиции.

    :param category_id: ID выбранного жанра.
    :param year_from: Начальный год диапазона.
    :param year_to: Конечный год диапазона.
    :param limit: Максимальное количество фильмов.
    :param offset: Количество пропускаемых фильмов.
    :return: Список найденных фильмов.
    """
    return get_films_by_category_id_and_year(
        category_id,
        year_from,
        year_to,
        limit,
        offset,
    )


def get_category_films_count(
    category_id,
    year_from,
    year_to
) -> int:
    """
    Возвращает количество фильмов
    выбранного жанра за указанный диапазон лет.
    """
    return get_films_count_by_category_id_and_year(
        category_id,
        year_from,
        year_to
    )
