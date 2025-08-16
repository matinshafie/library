import mysql.connector as sql
from dotenv import load_dotenv
import os
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from datetime import date

load_dotenv()


def get_connection() -> (PooledMySQLConnection | MySQLConnectionAbstract):
    return sql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
class Library:
    def __init__(self):
        self.__connection = get_connection()
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS library")
        self.__cursor.execute(f'USE library')
        self.__cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                book_id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(50) NOT NULL,
                author_id INT NOT NULL,
                published_year INT NOT NULL,
                added_date DATE NOT NULL
            )
        """
        )
        self.__cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS authors (
                author_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL
            )
        """
        )


    def add_book(self, title: str, author_id: int, published_year: int):
        self.__cursor.execute(
            "INSERT INTO books (title, author_id, published_year,added_date) VALUES (%s, %s, %s,CURDATE())",
            (title, author_id, published_year),
        )
        self.__connection.commit()

    def add_author(self, name: str):
        self.__cursor.execute("INSERT INTO authors (name) VALUES (%s)", (name,))
        self.__connection.commit()

    def remove_book(self, book_id: int):
        query = "DELETE FROM books WHERE book_id=%s"
        self.__cursor.execute(query, (book_id,))
        self.__connection.commit()

    def remove_author(self, author_id: int):
        query = "DELETE FROM authors WHERE author_id=%s"
        self.__cursor.execute(query, (author_id,))
        self.__connection.commit()

    def get_books(self) -> list[tuple]:
        self.__cursor.execute("SELECT * FROM books")
        results = self.__cursor.fetchall()

        return results

    def get_authors(self) -> list[tuple]:
        self.__cursor.execute("SELECT * FROM authors")
        results = self.__cursor.fetchall()

        return results

    def book_existence(self, book_id: int) -> bool:
        query = "SELECT 1 FROM books WHERE book_id=%s LIMIT 1"
        self.__cursor.execute(query, (book_id,))
        return self.__cursor.fetchone() is not None

    def author_existence(self, author_id: int) -> bool:
        query = "SELECT 1 FROM authors WHERE author_id=%s LIMIT 1"
        self.__cursor.execute(query, (author_id,))
        return self.__cursor.fetchone() is not None

    def search_book_by_id(self, book_id: int) -> tuple:
        query = "SELECT * FROM books WHERE book_id=%s"
        self.__cursor.execute(query, (book_id,))
        return self.__cursor.fetchone()

    def search_author_by_id(self, author_id: int) -> tuple:
        query = "SELECT * FROM authors WHERE author_id=%s"
        self.__cursor.execute(query, (author_id,))
        return self.__cursor.fetchone()

    def search_by_book_title(self, book_name: str) -> list[tuple]:
        if not book_name:
            return []
        query = "SELECT * FROM books WHERE title REGEXP %s"
        self.__cursor.execute(query, (book_name,))
        return self.__cursor.fetchall()

    def search_by_author_name(self, author_name: str) -> list[tuple]:
        query = "SELECT * FROM authors WHERE name REGEXP %s"
        if not author_name:
            return []
        self.__cursor.execute(query, (author_name,))
        return self.__cursor.fetchall()

    def search_book_by_author_name(self, author_name: str) -> list[tuple]:
        author_ids = tuple(
            map(lambda author: author[0], self.search_by_author_name(author_name))
        )
        if not author_ids:
            return []
        placeholders = ",".join(["%s"] * len(author_ids))
        query = f"SELECT * FROM books WHERE author_id IN ({placeholders})"
        self.__cursor.execute(query, author_ids)
        return self.__cursor.fetchall()

    def search_book_by_published_year(self, published_year: int) -> list[tuple]:
        query = "SELECT * FROM books WHERE published_year=%s"
        self.__cursor.execute(query, (published_year,))
        return self.__cursor.fetchall()

    def add_user_type(self,user_type:str,limit:int):
        query="INSERT INTO user_types (type,limit_borrow) VALUES (%s,%s)"
        self.__cursor.execute(query,(user_type,limit))
        self.__connection.commit()

class UserOperations:
    def __init__(self):
        self.__connection=get_connection()
        self.__cursor=self.__connection.cursor()
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS users")
        self.__cursor.execute(f'USE users')
        
        self.__cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_types (
                type_id INT PRIMARY KEY AUTO_INCREMENT,
                type VARCHAR(50) NOT NULL,
                limit_borrow INT NOT NULL
            )
        """
        )
        self.__cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                user_name VARCHAR(50) NOT NULL,
                type_id INT NOT NULL,
                password VARCHAR(8) NOT NULL,
                age INT NOT NULL,
                sign_up_date DATE NOT NULL,
                last_login DATE NOT NULL
            )
        """
        )
    
    def add_user_type(self,user_type:str,limit_borrow_book:int):
        query="INSERT INTO user_types (type,limit_borrow) VALUES (%s,%s)"
        self.__cursor.execute(query,(user_type,limit_borrow_book))
        self.__connection.commit()

    def remove_user_type(self,type_id:int):
        query="DELETE FROM user_types WHERE type_id=%s"
        self.__cursor.execute(query,(type_id,))
        self.__connection.commit()

    def add_user(self,first_name:str,
                last_name:str,
                user_name:str,
                type_id:int,
                password:str,
                age:int
            ):
        query="""
            INSERT INTO users (
                first_name,
                last_name,
                user_name,
                type_id,
                password,
                age,
                sign_up_date,
                last_login
            ) 
            VALUES (%s,%s,%s,%s,%s,%s,NOW(),NOW())
            """
        self.__cursor.execute(
            query,(
                first_name,last_name,user_name,type_id,password,age
                )
            )
        self.__connection.commit()

    def remove_user(self,user_id:int):
        query="DELETE FROM users WHERE user_id=%s"
        self.__cursor.execute(query,(user_id,))
        self.__connection.commit()

    def search_user_by_id(self,user_id:int)->tuple:
        query="SELECT * FROM users WHERE user_id = %s"
        self.__cursor.execute(query,(user_id,))
        return self.__cursor.fetchone()

    def search_user(
            self,
            user_name:str=None,
            age_range:list[int]=None,
            first_name:str=None,
            last_name:str=None,
            sign_up_date_range:list[date]=None,
            last_login_range:list[date]=None,
            )->list[tuple]:
        query="SELECT * FROM users"

        conditions=list[str]()
        params=list[str]()

        if user_name is not None:
            conditions.append("user_name LIKE %s")
            params.append(f"%{user_name}%")

        if age_range is not None:
            conditions.append("age BETWEEN %s AND %s")
            params.extend(age_range)

        if first_name is not None:
            conditions.append("first_name LIKE %s")
            params.append(f"%{first_name}%")

        if last_name is not None:
            conditions.append("last_name LIKE %s")
            params.append(f"%{last_name}%")

        if sign_up_date_range is not None:
            conditions.append("sign_up_date_range BETWEEN %s AND %s")
            params.extend(sign_up_date_range)

        if last_login_range is not None:
            conditions.append("last_login_range BETWEEN %s AND %s")
            params.extend(last_login_range)


        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        self.__cursor.execute(query,tuple(params))
        return self.__cursor.fetchall()