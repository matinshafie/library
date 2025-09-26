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

def generate_insert_query(column_names:list[str],values:list[str],table_name:str):
    query="INSERT INTO "+table_name
    columns=f" ({",".join(column_names)}) "
    place_holders=f"({",".join(["%s"]*len(column_names))}) "
    query+=columns
    query +=f"VALUES " + place_holders

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(values))
        conn.commit()

def add_book(author_id:int,title:str,number:int,published_year:str):
    column_names=["author_id","title","number","published_year"]
    values=[author_id,title,number,published_year]
    generate_insert_query(column_names,values,"books")

def add_author(first_name:str,last_name:str):
    column_names=["first_name","last_name"]
    values=[first_name,last_name]
    generate_insert_query(column_names,values,"authors")

def add_tag(tag:str):
    generate_insert_query(["tag"],[tag],"tags")
    
def borrow_book(book_id:int,client_id:int):
    column_names=["book_id","client_id"]
    values=[book_id,client_id]
    generate_insert_query(column_names,values,"borrowed_books")

def add_client(first_name:str,last_name:str,birth_date:str):
    column_names=["first_name","last_name","birth_date"]
    values=[first_name,last_name,birth_date]
    generate_insert_query(column_names,values,"clients")

def add_book_tag(book_id:int,tag_id:int):
    column_names=["book_id","tag_id"]
    values=[book_id,tag_id]
    generate_insert_query(column_names,values,"book_tag")

def generate_delete_query(primary_keys:list[str],values:list[str],table_name:str):
    query="DELETE FROM "+table_name+" WHERE "
    
    check_statements=list[str]()

    for key in primary_keys:
        check_statements.append(key+"=%s")
    query+=" AND ".join(check_statements)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(values))
        conn.commit()
    
def remove_author(author_id:int):
    generate_delete_query(["author_id"],[author_id],"authors")
    
def remove_book(book_id:int):
    generate_delete_query(["book_id"],[book_id],"books")

def remove_tag(tag_id:int):
    generate_delete_query(["tag_id"],[tag_id],"tags")

def remove_borrowed_book(borrowed_id:int):
    generate_delete_query(["borrowed_id"],[borrowed_id],"borrowed_books")

def remove_client(client_id:int):
    generate_delete_query(["client_id"],[client_id],"clients")

def remove_book_tag(book_id:int,tag_id:int):
    generate_delete_query(["book_id","tag_id"],[book_id,tag_id],"book_tag")

def generate_search_query(col_val_pairs:list[tuple],table_name:str)->list[tuple]:
    query=f"SELECT * FROM {table_name} "
    query_check_statements=list[str]()

    for column,value in col_val_pairs:
        if value is not None:
            query_check_statements.append(column+"=%s")

    if query_check_statements:
        query+="WHERE "

    query+=" AND ".join(query_check_statements)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                tuple([pair[1] for pair in col_val_pairs if pair[1] is not None])
                )
            return cursor.fetchall()

def search_books(
        book_id:int=None,
        author_id:int=None,
        title:str=None,
        published_year:str=None,
        )->list[tuple]:
    columns=["book_id","author_id","title","published_year"]
    values=[book_id,author_id,title,published_year]

    return generate_search_query(list(zip(columns,values)),"books")

def search_authors(
        author_id:int=None,
        first_name:str=None,
        last_name:str=None,
        )->list[tuple]:
    columns=["author_id","first_name","last_name"]
    values=[author_id,first_name,last_name]

    return generate_search_query(list(zip(columns,values)),"authors")

def search_book_tag(
        book_id:int=None,
        tag_id:int=None,
        )->list[tuple]:
    columns=["book_id","tag_id"]
    values=[book_id,tag_id]

    return generate_search_query(list(zip(columns,values)),"book_tag")

def search_tag(
        tag_id:int=None,
        tag:str=None,
        )->list[tuple]:
    columns=["tag_id","tag"]
    values=[tag_id,tag]

    return generate_search_query(list(zip(columns,values)),"tags")

def search_borrowed_books(
        borrowed_id:int=None,
        book_id:int=None,
        client_id:int=None
        )->list[tuple]:
    columns=["borrowed_id","book_id","client_id"]
    values=[borrowed_id,book_id,client_id]

    return generate_search_query(list(zip(columns,values)),"borrowed_books")

def search_clients(
        client_id:int=None,
        first_name:str=None,
        last_name:str=None,
        birth_date:str=None
        )->list[tuple]:
    columns=["client_id","first_name","last_name","birth_date"]
    values=[client_id,first_name,last_name,birth_date]

    return generate_search_query(list(zip(columns,values)),"clients")

def generate_existence_query(primary_keys:list[str],values:list[str],table_name:str)->bool:
    query=f"SELECT 1 FROM {table_name} WHERE "

    check_statements=list[str]()

    for key in primary_keys:
        check_statements.append(str(key)+"=%s")

    query+=" AND ".join(check_statements)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query,tuple(values))
            return bool(cursor.fetchone())

def book_id_exists(book_id:int)->bool:
    return generate_existence_query(["book_id"],[book_id],"books")

def author_id_exists(author_id:int)->bool:
    return generate_existence_query(["author_id"],[author_id],"authors")

def book_tag_id_exists(book_id:int,tag_id:int)->bool:
    return generate_existence_query(["book_id",tag_id],[book_id,tag_id],"book_tag")

def borrowed_id_exists(borrowed_id:int)->bool:
    return generate_existence_query(["borrowed_id"],[borrowed_id],"borrowed_bookss")

def client_id_exists(client_id:int)->bool:
    return generate_existence_query(["client_id"],[client_id],"clients")

def tag_id_exists(tag_id:int)->bool:
    return generate_existence_query(["tag_id"],[tag_id],"tags")