import json
import os
from typing import List, Dict, Optional


def singleton(class_):
    '''Декоратор для паттерна синглтон'''
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class Book:
    '''
    Класс Книга
    '''
    ids = set()

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        status: str = "в наличии",
        id: Optional[int] = None,
    ):
        '''
        Создание новой книги
        '''
        self.title = title
        self.author = author
        if id is not None:
            if id in self.ids:
                raise ValueError(f"ID {id} уже существует")
            self.id = id
            self.ids.add(id)
        else:
            self.id = self.new_id()
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        '''
        Представление объекта книги в виде словаря
        '''
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @classmethod
    def new_id(cls) -> int:
        '''
        Генерация нового id не совпадающего с уже занятыми по возрастанию с учетом пропусков
        '''
        id = 1
        while id in cls.ids:
            id += 1
        cls.ids.add(id)
        return id


@singleton
class BookDatabase:
    ''' 
    Класс для подключения к базе книг. 
    Использован паттерн синглтон для невозможности дублирования обращения к базе(ам).
    В данном проекте не обязательно, но в дальнейшем может сыграть.
    '''
    def __init__(self, books_file: str):
        '''
        Инициализация нового подключения
        '''
        self.books: List[Book] = []
        self.file = books_file
        self.load_file()

    def load_file(self) -> None:
        """Загружает книги из JSON файла."""
        if not os.path.exists(self.file):
            self.books = []
            print("Библиотека пуста.")
            return None
        try:
            with open(self.file, "r", encoding="utf-8") as file:
                json_data = json.load(file)
                for item in json_data:
                    book = Book(
                        id=item["id"],
                        title=item["title"],
                        author=item["author"],
                        year=item["year"],
                        status=item["status"],
                    )
                    self.books.append(book)
                n = len(self.books)
                print(f"Загружено {n} книг.")
        except json.JSONDecodeError as e:
            self.books = []
            print(e)
        except ValueError as e:
            self.books = []
            print(e)

    def save_books(self) -> None:
        """Сохраняет книги в JSON файл."""
        try:
            with open(self.file, "w", encoding="utf-8") as file:
                json.dump(
                    [book.to_dict() for book in self.books],
                    file,
                    ensure_ascii=False,
                    indent=4,
                )
        except Exception:
            print("Ошибка сохранения в JSON")

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет новую книгу в библиотеку."""
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def get_one_or_none(self, **criteria) -> Optional[Book]:
        """Ищет книгу по критериям"""
        for book in self.books:
            if all(getattr(book, key) == value for key, value in criteria.items()):
                return book
        return None

    def get_list_or_none(self, **criteria) -> Optional[List[Book]]:
        """Ищет список книг, удовлетворяющих критериям"""
        books = []
        for book in self.books:
            if all(str(getattr(book, key)).lower() == str(value).lower() for key, value in criteria.items()):
                books.append(book)
        if books:
            return books
        return None

    def delete_book(self, book_id: int) -> None:
        """Удаляет книгу из библиотеки по id."""
        book = self.get_one_or_none(id=book_id)
        if book:
            self.books.remove(book)
            print(f"Книга с id {book_id} удалена.")
        else:
            print(f"Книга с id {book_id} не найдена")

    def find_books(self, **criteria) -> None:
        '''
        Поиск и вывод книг по критериям
        '''
        books = self.get_list_or_none(**criteria)
        if books:
            n = len(books)
            print(f"Найдено {n} книг.")
            for book in books:
                print(book.to_dict())
        else:
            print("Ничего не найдено")

    def all_books(self) -> None:
        '''
        Вывод всех книг
        '''
        n = len(self.books)
        print(f"Всего в базе {n} книг.")
        for book in self.books:
            print(book.to_dict())

    def change_status(self, book_id: int, new_status: str) -> None:
        '''
        Изменение статуса книги по ID
        '''
        if new_status not in ["в наличии", "выдана"]:
            print(
                "Неверное значение статуса! Корректные значения: 'в наличии', 'выдана'."
            )
            return None
        book = self.get_one_or_none(id=book_id)
        if book is None:
            print(f"Книга с ID {book_id} не найдена!")
            return None
        book.status = new_status
        self.save_books()
        print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
