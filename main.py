import duckdb
from database import create_database
from button_click import handle_button_click

if __name__ == "__main__":
    # Verbindung zur DuckDB-Datenbank herstellen und die Datei "books.db" verwenden
    database = duckdb.connect(database='books.db')

    # Datenbank erstellen, falls sie noch nicht existiert
    create_database(database)

    print(database.sql("SELECT * FROM books;"))

    print("Was möchtest Du tun?")
    eingabe = input("Drücke \"s\", um nach einem bestehenden Buch zu suchen und \"h\", um ein neues Buch hinzuzufügen: ")

    if eingabe in ['s', 'h']:
        book_title = input("Gib den Titel des Buches ein: ")
        handle_button_click(database, eingabe, book_title)
    else:
        print("Ungültige Eingabe. Bitte starte das Programm neu.")