import json
import os
from math import ceil
from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


def on_reload(): # Рендерит template.html в index.html и сохраняет новый файл.
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html') # Python-скрипт находит HTML-шаблон.

    with open("books.json", encoding="utf8") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json) # достаю информацию о книгах.
    books_pages = list(chunked(books, 20))

    for i, book_page in enumerate(books_pages):
        separated_books = list(chunked(book_page, 2)) # делит books 
        
        #num_of_pages = book_page/i # кол-во страниц
        print(i, book_page)
        rendered_page = template.render(  # рендеринг template.html.
            separated_books = separated_books
        )

        with open(f'pages/index{i+1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page) # Сохранение файла.


os.makedirs("pages", exist_ok=True)
on_reload()

server = Server() # Создание сервера
server.watch('template.html', on_reload) # Команда которая следит за изменениями в файлах и после каждого изменения запускает консольную программу.
server.serve(root='.') # Запуск сервера.
