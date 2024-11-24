from library import BookDatabase

BOOK_DATABASE_URL = "books.json"


def main():
    db = BookDatabase(books_file=BOOK_DATABASE_URL)
    while True:
        print(
            "\nМеню:"
            "\n1. Добавить книгу"
            "\n2. Удалить книгу"
            "\n3. Найти книгу"
            "\n4. Показать все книги"
            "\n5. Изменить статус книги"
            "\n6. Выход"
        )
        try:
            choice = input("Выберите команду: ")
            if choice == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания: "))
                db.add_book(title, author, year)

            elif choice == "2":
                book_id = int(input("Введите id книги для удаления: "))
                db.delete_book(book_id)

            elif choice == "3":
                field = input("Введите поле для поиска (title, author, year): ")
                query = input("Введите значение для поиска: ")
                criteria = {field: query}
                db.find_books(**criteria)

            elif choice == "4":
                db.all_books()

            elif choice == "5":
                book_id = int(input("Введите id книги для изменения статуса: "))
                status = input("Введите новый статус (в наличии, выдана): ")
                db.change_status(book_id, status)

            elif choice == "6":
                break

            else:
                print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
