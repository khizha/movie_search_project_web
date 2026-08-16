from datetime import datetime
from functools import wraps
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from local_settings import (
    DATABASE_WRITE,
    MONGODB_COLLECTION,
    MONGODB_URL_WRITE,
)

from logger import logger

POPULAR_SEARCHES_LIMIT = 5
RECENT_SEARCHES_LIMIT = 5


def connect() -> MongoClient:
    """
        Создает подключение к серверу MongoDB.

        Использует строку подключения, указанную в настройках проекта.

        :return: Объект клиента MongoDB.
    """
    return MongoClient(MONGODB_URL_WRITE)


def get_collection() -> tuple[MongoClient, Collection]:
    """
    Возвращает подключение к MongoDB и коллекцию.

    Создает подключение к серверу, открывает указанную
    в настройках базу данных и возвращает объект коллекции.

    :return: Кортеж (client, collection).
    """
    client = connect()
    db = client[DATABASE_WRITE]
    collection = db[MONGODB_COLLECTION]
    return client, collection


def log_mongo_errors(default_return, raise_error=False):
    """
    Декоратор для обработки ошибок MongoDB.

    Перехватывает исключения PyMongoError,
    записывает информацию об ошибке в лог
    и возвращает значение, указанное
    в параметре default_return.

    Если raise_error=True, после записи ошибки
    в лог исключение передаётся дальше вызывающему
    коду.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except PyMongoError as error:
                logger.error(
                    f"Ошибка MongoDB в функции {func.__name__}: {error}"
                )

                if raise_error:
                    raise

                return default_return

        return wrapper

    return decorator


@log_mongo_errors(None)
def save_search_log(
    search_type: str,
    search_params: dict[str, Any],
    results_count: int,
) -> None:
    """
    Сохраняет информацию о выполненном поисковом запросе в MongoDB.

    Формирует документ с типом поиска, параметрами запроса,
    количеством найденных результатов и временем выполнения поиска,
    после чего записывает его в коллекцию MongoDB.

    :param search_type: Тип поиска (например, "keyword",
        "category_name_and_year").
    :param search_params: Параметры поискового запроса.
    :param results_count: Количество найденных фильмов.
    :return: None.
    """
    client = None

    try:
        client, collection = get_collection()

        normalized_search_params = search_params.copy()
        if search_type == "keyword":
            normalized_search_params["keyword"] = (
                normalized_search_params["keyword"].lower()
            )

        document = {
            "search_type": search_type,
            "search_params": normalized_search_params,
            "results_count": results_count,
            "created_at": datetime.now(),
        }

        collection.insert_one(document)

    finally:
        if client:
            client.close()


@log_mongo_errors([], raise_error=True)
def get_popular_searches() -> list[dict[str, Any]]:
    """
    Возвращает список из пяти самых популярных поисковых запросов.

    Популярность определяется частотой выполнения одинаковых запросов.
    Запрос считается одинаковым, если совпадают его тип (`search_type`)
    и параметры (`search_params`).

    При ошибке MongoDB исключение передаётся вызывающему коду
    для обработки на уровне приложения.

    :return: Список словарей с информацией о популярных поисковых
    запросах.
    """
    client = None

    try:
        client, collection = get_collection()

        # aggregation pipeline для подсчета популярных запросов
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "search_type": "$search_type",
                        "search_params": "$search_params",
                    },
                    "requests_count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                   "requests_count": -1
                }
            },
            {
                "$limit": POPULAR_SEARCHES_LIMIT
            },
            {
                "$project": {
                    "_id": 0,
                    "search_type": "$_id.search_type",
                    "search_params": "$_id.search_params",
                    "requests_count": 1,
                }
            }
        ]
        result = collection.aggregate(pipeline)

        return list(result)

    finally:
        if client:
            client.close()


@log_mongo_errors([], raise_error=True)
def get_recent_searches(limit: int = RECENT_SEARCHES_LIMIT) -> list[dict[str, Any]]:
    """
    Возвращает список последних уникальных поисковых запросов.

    Запросы сортируются по времени выполнения.
    Для каждого уникального сочетания типа и параметров запроса
    берется последняя по времени выполненная запись.
    Полученные запросы снова сортируются по времени
    и ограничиваются указанным количеством.

    При ошибке MongoDB исключение передаётся вызывающему коду
    для обработки на уровне приложения.

    :param limit: Максимальное количество уникальных запросов.
    :return: Список последних уникальных поисковых запросов.
    """
    client = None

    try:
        client, collection = get_collection()

        pipeline = [
            {
                "$sort": {
                    "created_at": -1
                }
            },
            {
                "$group": {
                    "_id": {
                        "search_type": "$search_type",
                        "search_params": "$search_params",
                    },
                    "search_type": {
                        "$first": "$search_type"
                    },
                    "search_params": {
                        "$first": "$search_params"
                    },
                    "results_count": {
                        "$first": "$results_count"
                    },
                    "created_at": {
                        "$first": "$created_at"
                    },
                }
            },
            {
                "$sort": {
                    "created_at": -1
                }
            },
            {
                "$limit": limit
            },
            {
                "$project": {
                    "_id": 0,
                    "search_type": 1,
                    "search_params": 1,
                    "results_count": 1,
                    "created_at": 1,
                }
            }
        ]

        result = collection.aggregate(pipeline)

        return list(result)

    finally:
        if client:
            client.close()


if __name__ == "__main__":
    result = get_recent_searches()

    print("MongoDB smoke test:")
    print(f"Получено последних поисковых запросов: {len(result)}")

    for item in result:
        print(f"- {item['search_type']}: {item['search_params']}")