import os
import mysql.connector as sql
from dotenv import load_dotenv
from mysql.connector.errors import Error

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

def get_connection()->sql.MySQLConnection:
    try:
        conn=sql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        if conn.is_connected():
            return conn
        else:
            raise Error("could not connect to database")
    except Error as e:
        print("error connecting to database " + e)
        raise

def initialize_schema():
    try:
        with open("./schema_query.txt","r") as schema_query:
            query_statements=schema_query.read().split(";")

            with get_connection() as conn:
                with conn.cursor() as cursor:
                    for statement in query_statements:
                        statement=statement.strip()
                        if statement!="":
                            cursor.execute(statement)
                conn.commit()
    except Error as e:
        print("error executing schema script:")
        raise
    except Exception:
        print("an unexpected error occured:")
        raise
            

def add_book(author_id:int,title:str,number:int,published_year:str):
    query="""
    INSERT INTO books 
        (author_id,title,number,published_year) 
    VALUES (%s,%s,%s,%s)
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (author_id,title,number,published_year))
        conn.commit()

def add_author(first_name:str,last_name:str):
    query="""
    INSERT INTO authors 
        (first_name,last_name) 
    VALUES (%s,%s)
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (first_name,last_name))
        conn.commit()

def add_tag(tag:str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tags (tag) VALUES (%s)",
                (tag,)
                )
            conn.commit()
    
def borrow_book(book_id:int,client_id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO borrowed_books (book_id,client_id) VALUES (%s,%s)",
                (book_id,client_id)
                )
        conn.commit()

def add_client(first_name:str,last_name:str,birth_date:str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO clients (first_name,last_name,birth_date) VALUES (%s,%s,%s)",
                (first_name,last_name,birth_date)
                )
        conn.commit()

def add_book_tag(book_id:int,tag_id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO book_tag (book_id,tag_id) VALUES (%s,%s)",
                (book_id,tag_id)
                )
        conn.commit()
    
def remove_author(author_id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM authors WHERE author_id = %s",(author_id,)
                )
        conn.commit()
    
def remove_book(book_id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE book_id=%s",(book_id,))
        conn.commit()

def remove_tag(tag_id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tags WHERE tag_id=%s",(tag_id,))
        conn.commit()

def remove_borrowed_book(borrowed_id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM borrowed_books WHERE borrowed_id=%s",
                (borrowed_id,)
                )
        conn.commit()

def remove_client(client_id:int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM clients WHERE client_id=%s",
                (client_id,)
                )
        conn.commit()

def remove_book_tag(book_id:int,tag_id:int):
    query="DELETE FROM book_tag WHERE book_id=%s AND tag_id=%s"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,(book_id,tag_id))
        conn.commit()

def search_books(
        book_id:int=None,
        author_id:int=None,
        title:str=None,
        published_year:str=None,
        )->list[tuple]:
    book_search_columns=[]
    book_column_names=list[str]()
    if book_id is not None:
        book_search_columns.append(str(book_id))
        book_column_names.append("book_id=%s")
    if author_id is not None:
        book_search_columns.append(str(author_id))
        book_column_names.append("author_id=%s")
    if title is not None:
        book_search_columns.append(title)
        book_column_names.append("title=%s")
    if published_year is not None:
        book_search_columns.append(published_year)
        book_column_names.append("published_year=%s")

    query="SELECT * FROM books"
    if book_column_names:
        query+=" WHERE "
    query+=" AND ".join(book_column_names)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(book_search_columns))
            return cursor.fetchall()

def search_authors(
        author_id:int=None,
        first_name:str=None,
        last_name:str=None,
        )->list[tuple]:
    author_search_columns=[]
    author_column_names=list[str]()
    if author_id is not None:
        author_search_columns.append(str(author_id))
        author_column_names.append("author_id=%s")
    if first_name is not None:
        author_search_columns.append(first_name)
        author_column_names.append("first_name=%s")
    if last_name is not None:
        author_search_columns.append(last_name)
        author_column_names.append("last_name=%s")

    query="SELECT * FROM authors"
    if author_column_names:
        query+=" WHERE "
    query+=" AND ".join(author_column_names)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(author_search_columns))
            return cursor.fetchall()

def search_book_tag(
        book_id:int=None,
        tag_id:int=None,
        )->list[tuple]:
    book_tag_search_columns=[]
    book_tag_column_names=list[str]()
    if book_id is not None:
        book_tag_search_columns.append(str(book_id))
        book_tag_column_names.append("book_id=%s")
    if tag_id is not None:
        book_tag_search_columns.append(str(tag_id))
        book_tag_column_names.append("tag_id=%s")

    query="SELECT * FROM book_tag"
    if book_tag_column_names:
        query+=" WHERE "
    query+=" AND ".join(book_tag_column_names)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(book_tag_search_columns))
            return cursor.fetchall()

def search_tag(
        tag_id:int=None,
        tag:str=None,
        )->list[tuple]:
    tag_search_columns=[]
    tag_column_names=list[str]()
    if tag_id is not None:
        tag_search_columns.append(str(tag_id))
        tag_column_names.append("tag_id=%s")
    if tag is not None:
        tag_search_columns.append(tag)
        tag_column_names.append("tag_id=%s")

    query="SELECT * FROM tags"
    if tag_column_names:
        query+=" WHERE "
    query+=" AND ".join(tag_column_names)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(tag_search_columns))
            return cursor.fetchall()

def search_borrowed_books(
        borrowed_id:int=None,
        book_id:int=None,
        client_id:int=None
        )->list[tuple]:
    borrowed_books_search_columns=[]
    borrowed_books_column_names=list[str]()
    if borrowed_id is not None:
        borrowed_books_search_columns.append(str(borrowed_id))
        borrowed_books_column_names.append("borrowed_id=%s")
    if book_id is not None:
        borrowed_books_search_columns.append(str(book_id))
        borrowed_books_column_names.append("book_id=%s")
    if client_id is not None:
        borrowed_books_search_columns.append(str(client_id))
        borrowed_books_column_names.append("client_id=%s")

    query="SELECT * FROM borrowed_books"
    if borrowed_books_column_names:
        query+=" WHERE "
    query+=" AND ".join(borrowed_books_column_names)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(borrowed_books_search_columns))
            return cursor.fetchall()

def search_clients(
        client_id:int=None,
        first_name:str=None,
        last_name:str=None,
        birth_date:str=None
        )->list[tuple]:
    clients_search_columns=[]
    clients_column_names=list[str]()
    if client_id is not None:
        clients_search_columns.append(str(client_id))
        clients_column_names.append("client_id=%s")
    if first_name is not None:
        clients_search_columns.append(first_name)
        clients_column_names.append("first_name=%s")
    if last_name is not None:
        clients_search_columns.append(last_name)
        clients_column_names.append("last_name=%s")
    if birth_date is not None:
        clients_search_columns.append(birth_date)
        clients_column_names.append("birth_date=%s")

    query="SELECT * FROM clients"
    if clients_column_names:
        query+=" WHERE "
    query+=" AND ".join(clients_column_names)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(clients_search_columns))
            return cursor.fetchall()

def book_id_exists(book_id:int)->bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM books WHERE book_id=%s",(book_id,))
            return bool(cursor.fetchone())

def author_id_exists(author_id:int)->bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM authors WHERE author_id=%s",(author_id,))
            return bool(cursor.fetchone())

def book_tag_id_exists(book_id:int,tag_id:int)->bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM book_tag b WHERE book_id=%s AND tag_id=%s",(book_id,tag_id))
            return bool(cursor.fetchone())

def borrowed_id_exists(borrowed_id:int)->bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM borrowed_books WHERE borrowed_id=%s",(borrowed_id,))
            return bool(cursor.fetchone())

def client_id_exists(client_id:int)->bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM clients WHERE client_id=%s",(client_id,))
            return bool(cursor.fetchone())

def tag_id_exists(tag_id:int)->bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM tags WHERE tag_id=%s",(tag_id,))
            return bool(cursor.fetchone())