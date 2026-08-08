from flask import Flask, render_template, request
from search_service import (
    search_by_keyword,
    get_categories,
    search_by_category,
)

from mongo_logger import get_popular_searches, save_search_log

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

    categories = get_categories()

    # Номер страницы.
    # Если page нет в URL — начинаем с первой страницы.
    page = int(request.args.get("page", 1))

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
        year_to
    )

    save_search_log(
        "genre",
        {
            "category_id": category_id,
            "year_from": year_from,
            "year_to": year_to
        },
        len(movies)
    )

    # Сколько фильмов показываем на одной странице
    per_page = 10

    # Вычисляем начало и конец нужной страницы
    start = (page - 1) * per_page
    end = start + per_page

    # Берём только 10 фильмов для текущей страницы
    page_movies = movies[start:end]

    # Есть ли следующая страница?
    has_next = end < len(movies)

    # Есть ли предыдущая страница?
    has_previous = page > 1

    return render_template(
        "genre.html",
        categories=categories,
        movies=page_movies,
        page=page,
        has_next=has_next,
        has_previous=has_previous,
        category_id=category_id,
        year_from=year_from,
        year_to=year_to
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