from flask import Flask, render_template, request, redirect, url_for
from search_service import (
    search_by_keyword,
    get_categories,
    search_by_category,
    get_category_films_count,
)

from mongo_logger import get_popular_searches, save_search_log

# количество фильмов на странице при постраничном выводе
RESULTS_PER_PAGE = 10

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    #return "<h2>Страница поиска по ключевому слову</h2>"
    if request.method == "POST":
        keyword = request.form["keyword"]

        # нажали поиск при незаполненном ключевом слове
        if not keyword.strip():
            return render_template(
                "search.html",
                error="Введите слово для поиска"
            )

        # Ищем фильмы в sql бд
        movies = search_by_keyword(keyword)

        # Сохраняем информацию о поиске в MongoDB
        save_search_log(
            "keyword",
            {"keyword": keyword},
            len(movies)
        )

        return render_template(
            "search.html",
            keyword=keyword,
            movies=movies
        )


    return render_template("search.html")


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

        # POST происходит только при нажатии «Найти», поэтому сохраняем историю здесь
        save_search_log(
            "genre",
            {
                "category_id": category_id,
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

    return render_template(
        "popular.html",
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)