import json
import os
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


def on_reload(): 
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html') 

    with open("books.json", encoding="utf8") as my_file:
        books_json = my_file.read()
    books = json.loads(books_json) 
    books_pages = list(chunked(books, 20))
    pages_count = len(books_pages)

    for i, book_page in enumerate(books_pages): 
        separated_books = list(chunked(book_page, 2)) 
        page_number = i+1

        rendered_page = template.render( 
            separated_books = separated_books,
            pages_count = pages_count,
            page_number = page_number
        )

        with open(f'pages/index{page_number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


os.makedirs("pages", exist_ok=True)
on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.', default_filename="pages/index1.html")
