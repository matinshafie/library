import mysql.connector as sql
from dotenv import load_dotenv
import os

load_dotenv()


class Library:
    def __init__(self):
        self.connection = sql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS library")
        self.cursor.execute(f'USE {os.getenv("DB_NAME")}')
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
