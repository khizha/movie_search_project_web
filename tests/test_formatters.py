from formatters import (
    format_search_params,
    format_search_description,
    format_search_type,
)


def test_format_search_params_keyword():
    """
    Проверяет форматирование параметров поиска по ключевому слову.
    """
    item = {
        "search_type": "keyword",
        "search_params": {
            "keyword": "matrix"
        }
    }

    result = format_search_params(item)

    assert result == "matrix"


def test_format_search_description_keyword():
    """
    Проверяет форматирование описания поиска по ключевому слову.
    """
    item = {
        "search_type": "keyword",
        "search_params": {
            "keyword": "matrix"
        }
    }

    result = format_search_description(item)

    assert result == 'Ключевое слово: "matrix"'


def test_format_search_type_keyword():
    """
    Проверяет преобразование типа поиска по ключевому слову
    в понятное для пользователя описание.
    """
    result = format_search_type("keyword")

    assert result == "По ключевому слову"


def test_format_search_params_category():
    """
    Проверяет форматирование параметров поиска по жанру и годам.
    """
    item = {
        "search_type": "category_name_and_year",
        "search_params": {
            "category_name": "Comedy",
            "year_from": 2000,
            "year_to": 2010
        }
    }

    result = format_search_params(item)

    assert result == "Comedy (2000-2010)"


def test_format_search_description_category():
    """
    Проверяет форматирование описания поиска по жанру и годам.
    """
    item = {
        "search_type": "category_name_and_year",
        "search_params": {
            "category_name": "Comedy",
            "year_from": 2000,
            "year_to": 2010
        }
    }

    result = format_search_description(item)

    assert result == "Жанр: Comedy (2000-2010)"


def test_format_search_type_category():
    """
    Проверяет преобразование типа поиска по жанру и годам
    в понятное для пользователя описание.
    """
    result = format_search_type("category_name_and_year")

    assert result == "По жанру и годам"