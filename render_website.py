import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
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
    separated_books = list(chunked(books, 2)) # делит books 

    rendered_page = template.render(  # рендеринг template.html.
        separated_books = separated_books
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page) # Сохранение файла.


server = Server() # Создание сервера
server.watch('template.html',on_reload) # Команда которая следит за изменениями в файлах и после каждого изменения запускает консольную программу.
server.serve(root='.') # Запуск сервера.
