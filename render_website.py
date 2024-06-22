import json
import argparse
import os
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


def on_reload():
    parser = argparse.ArgumentParser(
        description="Запускает сервер для сайта с книгами"
    )
    parser.add_argument("--file_path", help="Ваш путь до json файла", default="static/books.json")
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html") 

    with open(args.file_path, encoding="utf8") as my_file:
        books = json.load(my_file)
    books_pages_limit = 20
    books_pages = list(chunked(books, books_pages_limit))
    pages_count = len(books_pages)

    for page_number, book_page in enumerate(books_pages, 1):
        books_row_limit = 2
        separated_books = list(chunked(book_page, books_row_limit)) 

        rendered_page = template.render( 
            separated_books = separated_books,
            pages_count = pages_count,
            page_number = page_number
        )

        with open(f"pages/index{page_number}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    os.makedirs("pages", exist_ok=True)
    on_reload()

    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="pages/index1.html")


if __name__ == '__main__':
    main()
