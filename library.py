import mysql.connector as sql
from dotenv import load_dotenv
import os
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract

load_dotenv()


def get_connection() -> (PooledMySQLConnection | MySQLConnectionAbstract):
    return sql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
class Library:
    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS library")
        self.cursor.execute(f'USE library')
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                book_id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(50) NOT NULL,
                author_id INT NOT NULL,
                published_year INT NOT NULL
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS authors (
                author_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL
            )
        """
        )


    def add_book(self, title: str, author_id: int, published_year: int):
        self.cursor.execute(
            "INSERT INTO books (title, author_id, published_year) VALUES (%s, %s, %s)",
            (title, author_id, published_year),
        )
        self.connection.commit()

    def add_author(self, name: str):
        self.cursor.execute("INSERT INTO authors (name) VALUES (%s)", (name,))
        self.connection.commit()

    def remove_book(self, book_id: int):
        query = "DELETE FROM books WHERE book_id=%s"
        self.cursor.execute(query, (book_id,))
        self.connection.commit()

    def remove_author(self, author_id: int):
        query = "DELETE FROM authors WHERE author_id=%s"
        self.cursor.execute(query, (author_id,))
        self.connection.commit()

    def get_books(self) -> list[tuple]:
        self.cursor.execute("SELECT * FROM books")
        results = self.cursor.fetchall()

        return results

    def get_authors(self) -> list[tuple]:
        self.cursor.execute("SELECT * FROM authors")
        results = self.cursor.fetchall()

        return results

    def book_existence(self, book_id: int) -> bool:
        query = "SELECT 1 FROM books WHERE book_id=%s LIMIT 1"
        self.cursor.execute(query, (book_id,))
        return self.cursor.fetchone() is not None

    def author_existence(self, author_id: int) -> bool:
        query = "SELECT 1 FROM authors WHERE author_id=%s LIMIT 1"
        self.cursor.execute(query, (author_id,))
        return self.cursor.fetchone() is not None

    def search_book_by_id(self, book_id: int) -> tuple:
        query = "SELECT * FROM books WHERE book_id=%s"
        self.cursor.execute(query, (book_id,))
        return self.cursor.fetchall()

    def search_author_by_id(self, author_id: int) -> tuple:
        query = "SELECT * FROM authors WHERE author_id=%s"
        self.cursor.execute(query, (author_id,))
        return self.cursor.fetchone()

    def search_by_book_title(self, book_name: str) -> list[tuple]:
        if not book_name:
            return []
        query = "SELECT * FROM books WHERE title REGEXP %s"
        self.cursor.execute(query, (book_name,))
        return self.cursor.fetchall()

    def search_by_author_name(self, author_name: str) -> list[tuple]:
        query = "SELECT * FROM authors WHERE name REGEXP %s"
        if not author_name:
            return []
        self.cursor.execute(query, (author_name,))
        return self.cursor.fetchall()

    def search_book_by_author_name(self, author_name: str) -> list[tuple]:
        author_ids = tuple(
            map(lambda author: author[0], self.search_by_author_name(author_name))
        )
        if not author_ids:
            return []
        placeholders = ",".join(["%s"] * len(author_ids))
        query = f"SELECT * FROM books WHERE author_id IN ({placeholders})"
        self.cursor.execute(query, author_ids)
        return self.cursor.fetchall()

    def search_book_by_published_year(self, published_year: int) -> list[tuple]:
        query = "SELECT * FROM books WHERE published_year=%s"
        self.cursor.execute(query, (published_year,))
        return self.cursor.fetchall()

    def add_user_type(self,user_type:str,limit:int):
        query="INSERT INTO user_types (type,limit_borrow) VALUES (%s,%s)"
        self.cursor.execute(query,(user_type,limit))
        self.connection.commit()