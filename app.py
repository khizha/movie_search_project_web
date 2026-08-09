from flask import Flask, render_template, request, redirect, url_for
from search_service import (
    search_by_keyword,
    get_categories,
    search_by_category,
    get_category_films_count,
    get_keyword_films_count,
)

from mongo_logger import get_popular_searches, get_recent_searches, save_search_log

from formatters import (
    format_search_description,
    format_search_type,
)

# количество фильмов на странице при постраничном выводе
RESULTS_PER_PAGE = 10

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search", methods=["GET", "POST"])
def search():

    # Получаем номер текущей страницы из URL.
    # Если page нет в URL — начинаем с первой страницы.
    page = request.args.get("page", 1, type=int)

    # Сколько фильмов показываем на одной странице.
    per_page = RESULTS_PER_PAGE

    # Вычисляем, сколько фильмов нужно пропустить.
    # Страница 1: offset=0, страница 2: offset=10, страница 3: offset=20.
    offset = (page - 1) * per_page

    if request.method == "POST":

        keyword = request.form["keyword"]

        # Нажали поиск при незаполненном ключевом слове.
        if not keyword.strip():
            return render_template(
                "search.html",
                error="Введите слово для поиска"
            )

    else:

        # Получаем ключевое слово из URL при переходе между страницами.
        keyword = request.args.get("keyword")

        if not keyword:
            return render_template("search.html")

    # Ищем фильмы в SQL-базе.
    movies = search_by_keyword(
        keyword,
        per_page,
        offset
    )

    # Получаем общее количество фильмов,
    # найденных по ключевому слову.
    total = get_keyword_films_count(keyword)

    # Считаем, сколько страниц нужно для вывода всех фильмов.
    total_pages = (total + per_page - 1) // per_page

    # Определяем наличие кнопок навигации.
    has_previous = page > 1
    has_next = page < total_pages

    # Если пользователь выполнил новый поиск,
    # сохраняем его в MongoDB и переходим на первую страницу.
    if request.method == "POST":

        save_search_log(
            "keyword",
            {"keyword": keyword},
            total
        )

        return redirect(
            url_for(
                "search",
                keyword=keyword,
                page=1
            )
        )

    return render_template(
        "search.html",
        keyword=keyword,
        movies=movies,
        page=page,
        has_previous=has_previous,
        has_next=has_next
    )

@app.route("/genre", methods=["GET", "POST"])
def genre():

    # проверяем, на какой мы странице. если в URL есть ?page, значит страница не первая.
    # если page нет, значит это первая страница
    page = request.args.get("page", 1, type=int)

    per_page = RESULTS_PER_PAGE

    # page 1: offset=0, page 2: offset=10, page 3: offset=20
    offset = (page - 1) * per_page


    categories = get_categories()

    if request.method == "POST":

        category_id = request.form["category_id"]
        year_from = int(request.form["year_from"])
        year_to = int(request.form["year_to"])

    else:
        # Если пользователь нажал "Следующая" или "Предыдущая",
        # получаем данные из URL.
        category_id = request.args.get("category_id")
        year_from = request.args.get("year_from")
        year_to = request.args.get("year_to")

        if category_id is None:
            return render_template(
                "genre.html",
                categories=categories
            )

        year_from = int(year_from)
        year_to = int(year_to)

    # Проверяем диапазон годов
    if year_from > year_to:
        return render_template(
            "genre.html",
            categories=categories,
            error="Начальный год не может быть больше конечного",
            year_from=year_from,
            year_to=year_to
        )

    # Получаем фильмы из MySQL
    movies = search_by_category(
        category_id,
        year_from,
        year_to,
        per_page,
        offset
    )

    # Получаем количество фильмов
    total = get_category_films_count(
        category_id,
        year_from,
        year_to
    )

    # Считаем, сколько страниц нужно для выводна всех фильмоы
    # 60 фильмоы - 6 страниц, 61 фильм - 7 страниц...
    total_pages = (total + per_page - 1) // per_page


    # page 1 из 7 → Следующая есть
    # page 2 из 7 → обе есть
    # page 7 из 7 → Предыдущая есть, Следующей нет
    has_previous = page > 1
    has_next = page < total_pages

    # После нового поиска переходим на первую страницу
    # и передаём параметры поиска в URL.
    if request.method == "POST":
        # Находим название выбранного жанра по его ID.
        category_name = next(
            category["category"]
            for category in categories
            if str(category["category_id"]) == str(category_id)
        )

        # Сохраняем новый поиск в MongoDB
        # в том же формате, что и консольное приложение.
        save_search_log(
            "category_name_and_year",
            {
                "category_name": category_name,
                "year_from": year_from,
                "year_to": year_to
            },
            total
        )

        return redirect(
            url_for(
                "genre",
                category_id=category_id,
                year_from=year_from,
                year_to=year_to,
                page=1
            )
        )

    # Передаём в шаблон результаты поиска и данные для постраничной навигации.
    return render_template(
        "genre.html",
        categories=categories,
        movies=movies,
        category_id=category_id,
        year_from=year_from,
        year_to=year_to,
        page=page,
        has_previous=has_previous,
        has_next=has_next
    )



@app.route("/popular")
def popular():

    results = get_popular_searches()

    # categories = get_categories()
    #
    # category_names = {
    #     str(category["category_id"]): category["category"]
    #     for category in categories
    # }

    for item in results:
        # if item["search_type"] == "genre":
        #     category_id = str(item["search_params"]["category_id"])
        #     item["search_params"]["category_name"] = (
        #         category_names.get(category_id, "Неизвестный жанр")
        #     )

        item["search_type_description"] = format_search_type(
            item["search_type"]
        )

        item["search_description"] = format_search_description(item)

    return render_template(
        "popular.html",
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)