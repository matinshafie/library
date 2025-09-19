import os
import mysql.connector as sql
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

try:
    conn = sql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    if conn.is_connected():
        if __name__ == "__main__":
            print("successfuly connected to mysql server")

        cursor=conn.cursor()
except:
    if __name__=="__main__":
        print("error not connected to mysql server")

def initialize_schema():
    query="""-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema library
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema library
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `library` ;
USE `library` ;

-- -----------------------------------------------------
-- Table `library`.`authors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`authors` (
  `author_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`author_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `library`.`tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`tags` (
  `tag_id` INT NOT NULL AUTO_INCREMENT,
  `tag` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`tag_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `library`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`books` (
  `book_id` INT NOT NULL AUTO_INCREMENT,
  `author_id` INT NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `published_year` DATE NOT NULL,
  `number` INT NOT NULL,
  PRIMARY KEY (`book_id`),
  INDEX `fk_books_author_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_books_author`
    FOREIGN KEY (`author_id`)
    REFERENCES `library`.`authors` (`author_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `library`.`book_tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`book_tag` (
  `tag_id` INT NOT NULL,
  `book_id` INT NOT NULL,
  INDEX `fk_books_tags_book_tags1_idx` (`tag_id` ASC) VISIBLE,
  INDEX `fk_books_tags_books1_idx` (`book_id` ASC) VISIBLE,
  CONSTRAINT `fk_books_tags_book_tags1`
    FOREIGN KEY (`tag_id`)
    REFERENCES `library`.`tags` (`tag_id`),
  CONSTRAINT `fk_books_tags_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `library`.`books` (`book_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `library`.`clients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`clients` (
  `client_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `birth_date` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`client_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `library`.`borrowed_books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library`.`borrowed_books` (
  `borrowed_id` INT NOT NULL AUTO_INCREMENT,
  `book_id` INT NOT NULL,
  `client_id` INT NOT NULL,
  PRIMARY KEY (`borrowed_id`),
  INDEX `fk_borrowed_books_books1_idx` (`book_id` ASC) VISIBLE,
  INDEX `fk_borrowed_books_clients1_idx` (`client_id` ASC) VISIBLE,
  CONSTRAINT `fk_borrowed_books_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `library`.`books` (`book_id`),
  CONSTRAINT `fk_borrowed_books_clients1`
    FOREIGN KEY (`client_id`)
    REFERENCES `library`.`clients` (`client_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
"""
    cursor.execute(query)

cursor.execute("USE library")

def add_book(author_id:int,title:str,number:int,published_year:str):
    query="""
    INSERT INTO books 
        (author_id,title,number,published_year) 
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(query, (author_id,title,number,published_year))
    conn.commit()

def add_author(first_name:str,last_name:str):
    query="""
    INSERT INTO authors 
        (first_name,last_name) 
    VALUES (%s,%s)
    """

    cursor.execute(query, (first_name,last_name))
    conn.commit()

def add_tag(tag:str):
    cursor.execute(
        "INSERT INTO tags (tag) VALUES (%s)",
        (tag,)
        )
    
def borrow_book(book_id:int,client_id:int):
    cursor.execute(
        "INSERT INTO borrowed_books (book_id,client_id) VALUES (%s,%s)",
        (book_id,client_id)
        )
    conn.commit()

def add_client(first_name:str,last_name:str,birth_date:str):
    cursor.execute(
        "INSERT INTO clients (first_name,last_name,birth_date) VALUES (%s,%s,%s)",
        (first_name,last_name,birth_date)
        )
    conn.commit()

def add_book_tag(book_id:int,tag_id:int):
    cursor.execute(
        "INSERT INTO book_tag (book_id,tag_id) VALUES (%s,%s)",
        (book_id,tag_id)
        )
    conn.commit()
    
def remove_author(author_id:int):
    cursor.execute(
        "DELETE FROM authors WHERE author_id = %s",(author_id,)
        )
    conn.commit()
    
def remove_book(book_id:int):
    cursor.execute("DELETE FROM books WHERE book_id=%s",(book_id,))
    conn.commit()

def remove_tag(tag_id:int):
    cursor.execute("DELETE FROM tags WHERE tag_id=%s",(tag_id,))
    conn.commit()

def remove_borrowed_book(borrowed_id:int):
    cursor.execute("DELETE FROM borrowed_books WHERE borrowed_id=%s",(borrowed_id,))
    conn.commit()

def remove_client(client_id:int):
    cursor.execute("DELETE FROM clients WHERE client_id=%s",(client_id,))
    conn.commit()

def remove_book_tag(book_id:int,tag_id:int):
    query="DELETE FROM book_tag WHERE book_id=%s AND tag_id=%s"
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
    cursor.execute(query,tuple(book_tag_search_columns))
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
    cursor.execute(query,tuple(clients_search_columns))
    return cursor.fetchall()

def book_id_exists(book_id:int)->bool:
    cursor.execute("SELECT 1 FROM books WHERE book_id=%s",(book_id,))
    return bool(cursor.fetchone())

def author_id_exists(author_id:int)->bool:
    cursor.execute("SELECT 1 FROM authors WHERE author_id=%s",(author_id,))
    return bool(cursor.fetchone())

def book_tag_id_exists(book_id:int,tag_id:int)->bool:
    cursor.execute("SELECT 1 FROM book_tag b WHERE book_id=%s AND tag_id=%s",(book_id,tag_id))
    return bool(cursor.fetchone())

def borrowed_id_exists(borrowed_id:int)->bool:
    cursor.execute("SELECT 1 FROM borrowed_books WHERE borrowed_id=%s",(borrowed_id,))
    return bool(cursor.fetchone())

def client_id_exists(client_id:int)->bool:
    cursor.execute("SELECT 1 FROM clients WHERE client_id=%s",(client_id,))
    return bool(cursor.fetchone())

def tag_id_exists(tag_id:int)->bool:
    cursor.execute("SELECT 1 FROM tags WHERE tag_id=%s",(tag_id,))
    return bool(cursor.fetchone())
