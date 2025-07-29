import mysql.connector as sql


class Library:
    def __init__(self):
        self.connection = sql.connect(
            host='',
            user='',
            password='',
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS library")
        self.cursor.execute("USE library")
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

    def get_books(self) -> list[tuple]:
        self.cursor.execute("SELECT * FROM books")
        results = self.cursor.fetchall()

        return results

    def get_authors(self) -> list[tuple]:
        self.cursor.execute("SELECT * FROM authors")
        results = self.cursor.fetchall()

        return results

    def search_book_by_id(self,book_id:)