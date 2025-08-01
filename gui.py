from library import Library


lib = Library()


def show_options():
    print("1.show books")
    print("2.show authors")
    print("3.add book")
    print("4.add author")
    print("5.remove book")
    print("6.remove author")
    print("7.exit")


def get_prompt(prompt: str) -> str:
    return input(prompt)


def add_book():
    title = get_prompt("enter title: ")
    author_id = get_number("enter author id: ")
    published_year = get_number("enter published year: ")

    lib.add_book(title, author_id, published_year)


def get_number(prompt: str) -> int:
    while True:
        try:
            number = int(get_prompt(prompt))
            return number
        except ValueError:
            print("invalid input")


def remove_book():
    book_id = get_number("enter book id: ")
    if lib.book_existence(book_id):
        lib.remove_book(book_id)
    else:
        print("book doesn't exist")


def remove_author():
    author_id = get_number("enter author id: ")
    if lib.author_existence(author_id):
        lib.remove_author(author_id)
    else:
        print("book doesn't exist")


def show_books():
    for num, (book_id, title, author_id, published_year) in enumerate(
        lib.get_books(), 1
    ):
        print(
            f"{num}.id:{book_id}-title:{title}-author:{author_id}-published:{published_year}"
        )
    print()


def show_authors():
    for num, (author_id, name) in enumerate(lib.get_authors()):
        print(f"{num}.id:{author_id}-name:{name}")
    print()


while True:
    show_options()
    print()

    number = get_number("enter number for operation: ")
    print()

    if number == 1:
        show_books()
    elif number == 2:
        show_authors()
    elif number == 3:
        add_book()
        print()
    elif number == 4:
        lib.add_author(get_prompt("enter author's name: "))
        print()
    elif number == 5:
        show_books()
        remove_book()
        print()
    elif number == 6:
        show_authors()
        remove_author()
        print()
    elif number == 7:
        break
    else:
        print("invalid operation")
