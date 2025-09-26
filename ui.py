import database as db
from datetime import datetime,date

db.initialize_schema()


def show_options():
    print("1-book options")
    print("2-author options")
    print("3-book tag options")
    print("4-tags options")
    print("5-borrowed books options")
    print("6-clients options")
    print("7-exit")
    print()

def get_prompt(prompt:str,in_len:range=None,allowed_null:bool=False)->str:
    while True:
        user_in=input(prompt).strip()
        if user_in=="" and allowed_null:
            return None
        if in_len is not None:
            if len(user_in) in in_len:
                return user_in
        else:
            return user_in
        print("please enter a valid value try again")
    

def get_integer(prompt:str,num_range:range=None,allowed_null:bool=False)->int:
    while True:
        try:
            user_in=input(prompt).strip()
            if user_in=="" and allowed_null:
                return None
            user_in=int(user_in)
            if num_range:
                if user_in not in num_range:
                    raise ValueError
            return user_in
        except ValueError:
            print("please enter an integer value or your value should be listed on the options")
            print("try again!")

def get_date(prompt:str)->date:
    while True:
        try:
            return datetime.strptime(get_prompt(prompt),"%Y-%m-%d").date()
        except ValueError:
            print("please enter the date correctly (like 2000-01-01)")

def print_authors(authors:list[tuple]):
    if not authors:
        print("there are no authors printed")
        return
    for num,(author_id,first_name,last_name) in enumerate(authors,1):
        print(f"{num}-id:{author_id}, full name:{first_name} {last_name}")
    print()

def print_books(books:list[tuple]):
    if not books:
        print("there are no books printed")
        return
    for num,(book_id,author_id,title,published_year,number) in enumerate(books,1):
        print(
            f"{num}-id:{book_id}, title:{title}, author id:{author_id}, published year:{published_year}, number:{number}"
            )
    print()
        
def print_book_tag(book_tags:list[tuple]):
    if not book_tags:
        print("there are no book tag printed")
        return
    for num,(book_id,tag_id) in enumerate(book_tags,1):
        print(
            f"{num}-book id:{book_id}, tag id:{tag_id}"
            )
        print()
        
def print_tags(tags:list[tuple]):
    if not tags:
        print("there are no authors printed")
        return
    for num,(tag_id,tag) in enumerate(tags,1):
        print(
            f"{num}-id:{tag_id}, tag:{tag}"
            )
    print()
        
def print_borrowed_books(borrowed_books:list[tuple]):
    if not borrowed_books:
        print("there are no borrowed books printed")
        return
    for num,(borrowed_id,book_id,client_id) in enumerate(borrowed_books,1):
        print(
            f"{num}-id:{borrowed_id}, book id:{book_id}, client id:{client_id}"
            )
    print()
        
def print_clients(clients:list[tuple]):
    if not clients:
        print("there are no clients printed")
        return
    for num,(client_id,first_name,last_name,birth_date) in enumerate(clients,1):
        print(
            f"{num}-id:{client_id}, full name:{first_name} {last_name}, birth date:{birth_date}"
            )
    print()

def show_operation_options(operations:list[str],for_option:str):
    for num,operation in enumerate(operations,1):
        print(f"{num}-{operation} {for_option}")
            
def show_book_options():
    show_operation_options(["add","remove","search","go back from"],"book")

def show_author_options():
    show_operation_options(["add","remove","search","go back from"],"author")

def show_book_tag_options():
    show_operation_options(["add","remove","search","go back from"],"book_tag")

def show_tag_options():
    show_operation_options(["add","remove","search","go back from"],"tag")

def show_borrowed_books_options():
    show_operation_options(["add","remove","search","go back from"],"borrowed_book")

def show_client_options():
    show_operation_options(["add","remove","search","go back from"],"client")

def add_book():
    title=get_prompt("enter title: ",range(1,100)).strip()
    author_id=get_integer("enter author id: ")
    if not db.author_id_exists(author_id):
        print("author id doesn't exist please try again later")
        return
    number=get_integer("enter the number of books: ")
    published_year=get_date("enter published date year: ")

    db.add_book(author_id,title,number,published_year)

def search_books():
    book_id=get_integer("enter book id: (or skip)",allowed_null=True)
    author_id=get_integer("enter author id: (or skip)",allowed_null=True)
    title=get_prompt("enter title: (or skip)",allowed_null=True)
    published_year=get_prompt("enter published year: (or skip)",allowed_null=True)
    print_books(db.search_books(book_id,author_id,title,published_year))

def remove_book():
    book_id=get_integer("enter book id: ")
    if db.book_id_exists(book_id):
        db.remove_book(book_id)
    else:
        print("book id doesn't exist")

def book_options():
    show_book_options()
    option=get_integer("enter option number: ",range(1,5))
    if option==1:
        add_book()
    elif option==2:
        remove_book()
    elif option==3:
        search_books()
    elif option==4:
        pass

def add_author():
    first_name=get_prompt("enter the first name: ",range(1,50)).strip()
    last_name=get_prompt("enter the last name: ",range(1,50)).strip()

    db.add_author(first_name,last_name)

def search_authors():
    author_id=get_integer("enter author id: (or skip)",allowed_null=True)
    first_name=get_prompt("enter first name: (or skip)",allowed_null=True)
    last_name=get_prompt("enter last name: (or skip)",allowed_null=True)
    print_authors(db.search_authors(first_name,author_id,last_name))

def remove_author():
    author_id=get_integer("enter author id: ")
    if db.author_id_exists(author_id):
        db.remove_author(author_id)
    else:
        print("author id doesn't exist")

def author_options():
    show_author_options()
    option=get_integer("enter option number: ",range(1,5))
    if option==1:
        add_author()
    elif option==2:
        remove_author()
    elif option==3:
        search_authors()
    elif option==4:
        pass

def add_book_tag():
    book_id=get_integer("enter book id: ")
    if not db.book_id_exists(book_id):
        print("book id doesn't exist please try again later")
        return
    tag_id=get_integer("enter tag id: ")
    if not db.tag_id_exists(tag_id):
        print("tag id doesn't exist please try again later")
        return

    db.add_book_tag(book_id,tag_id)

def search_book_tags():
    book_id=get_integer("enter book id: (or skip)",allowed_null=True)
    tag_id=get_integer("enter tag id: (or skip)",allowed_null=True)
    print_book_tag(db.search_book_tag(book_id,tag_id))

def remove_book_tag():
    book_id=get_integer("enter book id: ")
    tag_id=get_integer("enter tag id: ")
    if db.book_tag_id_exists(book_id,tag_id):
        db.remove_book_tag(book_id,tag_id)
    else:
        print("book tag ids doesn't exist")

def book_tag_options():
    show_book_tag_options()
    option=get_integer("enter option number: ",range(1,5))
    if option==1:
        add_book_tag()
    elif option==2:
        remove_book_tag()
    elif option==3:
        search_book_tags()
    elif option==4:
        pass

def add_tag():
    tag=get_prompt("enter book tag name: ",range(1,50)).strip()

    db.add_tag(tag)

def search_tag():
    tag_id=get_integer("enter tag id: (or skip)",allowed_null=True)
    tag=get_prompt("enter tag: (or skip)",allowed_null=True)
    print_tags(db.search_tag(tag_id,tag))

def remove_tag():
    tag_id=get_integer("enter tag id: ")
    if db.tag_id_exists(tag_id):
        db.remove_tag(tag_id)
    else:
        print("tag id doesn't exist")

def tag_options():
    show_tag_options()
    option=get_integer("enter option number: ",range(1,5))
    if option==1:
        add_tag()
    elif option==2:
        remove_tag()
    elif option==3:
        search_tag()
    elif option==4:
        pass

def borrow_book():
    book_id=get_integer("enter book id: ")
    if not db.book_id_exists(book_id):
        print("book id doesn't exist please try again later")
        return
    client_id=get_integer("enter client id: ")
    if not db.client_id_exists(client_id):
        print("client id doesn't exist please try again later")
        return

    db.borrow_book(book_id,client_id)

def search_borrowed_books():
    borrowed_id=get_integer("enter borrowed id: (or skip)",allowed_null=True)
    book_id=get_integer("enter book id: (or skip)",allowed_null=True)
    client_id=get_integer("enter client id: (or skip)",allowed_null=True)
    print_borrowed_books(db.search_borrowed_books(borrowed_id,book_id,client_id))

def remove_borrowed_book():
    borrowed_id=get_integer("enter borrowed id: ")
    if db.borrowed_id_exists(borrowed_id):
        db.remove_borrowed_book(borrowed_id)
    else:
        print("borrowed id doesn't exist")

def borrow_book_options():
    show_borrowed_books_options()
    option=get_integer("enter option number: ",range(1,5))
    if option==1:
        borrow_book()
    elif option==2:
        remove_borrowed_book()
    elif option==3:
        search_borrowed_books()
    elif option==4:
        pass

def add_client():
    first_name=get_prompt("enter the first name: ").strip()
    last_name=get_prompt("enter the last name: ").strip()
    birth_date=get_date("enter the birth date year: ")

    db.add_client(first_name,last_name,birth_date)

def search_clients():
    client_id=get_integer("enter client_id id: (or skip)",allowed_null=True)
    first_name=get_prompt("enter first name: (or skip)",allowed_null=True)
    last_name=get_prompt("enter last name: (or skip)",allowed_null=True)
    print_clients(db.search_clients(client_id,first_name,last_name))

def remove_client():
    client_id=get_integer("enter client id: ")
    if db.client_id_exists(client_id):
        db.remove_client(client_id)
    else:
        print("client id doesn't exist")

def client_options():
    show_client_options()
    option=get_integer("enter option number: ",range(1,5))
    if option==1:
        add_client()
    elif option==2:
        remove_client()
    elif option==3:
        search_clients()
    elif option==4:
        pass

def run_library():
    while True:
        show_options()
        option=get_integer("please enter option number: ",range(1,8))

        if option==1:
            book_options()
        elif option==2:
            author_options()
        elif option==3:
            book_tag_options()
        elif option==4:
            tag_options()
        elif option==5:
            borrow_book_options()
        elif option==6:
            client_options()
        elif option==7:
            break

# if __name__=="__main__":
#     run_library()