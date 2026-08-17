def format_search_params(item: dict) -> str:
    """
    Формирует строку параметров поискового запроса в кратком виде.

    :param item: словарь с информацией о поисковом запросе.
    :return: строка с параметрами поиска.
    """

    p = item["search_params"]

    if item["search_type"] == "keyword":
        return p["keyword"]

    elif item["search_type"] == "category_name_and_year":
        return f'{p["category_name"]} ({p["year_from"]}-{p["year_to"]})'

    return str(p)


def format_search_description(item: dict) -> str:
    """
    Возвращает поисковый запрос для вывода в таблице статистики
    в удобном для пользователя виде.
    """

    p = item["search_params"]

    if item["search_type"] == "keyword":
        return f'Ключевое слово: "{p["keyword"]}"'

    elif item["search_type"] == "category_name_and_year":
        return (
            f'Жанр: {p["category_name"]} '
            f'({p["year_from"]}-{p["year_to"]})'
        )

    return str(p)


def format_search_type(search_type: str) -> str:
    """
    Возвращает тип поискового запроса для вывода в таблице статистики
    в понятном для пользователя виде.
    """

    if search_type == "keyword":
        return "По ключевому слову"

    if search_type == "category_name_and_year":
        return "По жанру и годам"

    return search_type


if __name__ == "__main__":
    item = {
        "search_type": "keyword",
        "search_params": {
            "keyword": "ant"
        }
    }

    print("Formatters smoke test:")
    print(f"Параметры: {format_search_params(item)}")
    print(f"Описание: {format_search_description(item)}")
    print(f"Тип поиска: {format_search_type(item['search_type'])}")
