import unittest
import os
import json
from library import BookDatabase, Book


class TestBookDatabase(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл для тестов
        self.test_file = "test_books.json"
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump([], f)

        self.db = BookDatabase(books_file=self.test_file)

    def tearDown(self):
        # Удаляем временный файл после тестов
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        self.db.add_book("Test Book1", "Test Author1", 2023)
        self.assertEqual(len(self.db.books), 1)
        self.assertEqual(self.db.books[0].title, "Test Book1")

    def test_delete_book(self):
        self.db.add_book("Test Book2", "Test Author2", 2023)
        book_id = self.db.get_one_or_none(title="Test Book2").id
        self.db.delete_book(book_id)
        self.assertIsNone(self.db.get_one_or_none(id=book_id))

    def test_find_books(self):
        self.db.add_book("Test Book3", "Test Author3", 2023)
        books = self.db.get_list_or_none(title="Test Book3")
        self.assertIsNotNone(books)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Test Book3")

    def test_change_status(self):
        self.db.add_book("Test Book4", "Test Author4", 2023)
        book_id = self.db.books[0].id
        self.db.change_status(book_id, "выдана")
        self.assertEqual(self.db.books[0].status, "выдана")

    def test_save_books(self):
        self.db.add_book("Test Book5", "Test Author5", 2023)
        self.db.save_books()
        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), len(self.db.books))
        self.assertEqual(data[-1]["title"], "Test Book5")


if __name__ == "__main__":
    unittest.main()
