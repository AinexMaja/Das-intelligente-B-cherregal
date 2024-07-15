import duckdb
from led import flashLED

def handle_button_click(database, action, book_title):
    if action == 's':
        if book_title:
            print(f"Gefundene(s) Buch/Bücher: {book_title}")
            result = database.execute(f"SELECT * FROM books WHERE title LIKE '%{book_title}%'").fetchall()
            for row in result:
                print(row)
            positions = list(database.execute(f"SELECT position FROM books WHERE title LIKE '%{book_title}%'").fetchall())
            widths = list(database.execute(f"SELECT width FROM books WHERE title LIKE '%{book_title}%'").fetchall())
            print(positions, widths)
            flashLED(positions, widths)

    elif action == 'h':
        if book_title:
            print(f"Neuer Buchtitel: {book_title}")
            title = book_title
            author = input("Gib den Autor des Buches ein: ")
            year = int(input("Gib das Jahr des Buches ein: "))
            genre = input("Gib das Genre des Buches ein: ")
            width = float(input("Gib die Breite des Buches ein: "))
            height = float(input("Gib die Höhe des Buches ein: "))
            depth = float(input("Gib die Tiefe des Buches ein: "))
            row = int(input("Gib die Reihe des Buches ein: "))
            position = float(input("Gib die Position des Buches ein: "))
            isbn = input("Gib die ISBN des Buches ein: ")
            database.execute(f"""
                INSERT INTO books (title, author, year, genre, width, height, depth, row, position, isbn) VALUES
                ('{title}', '{author}', {year}, '{genre}', {width}, {height}, {depth}, {row}, {position}, '{isbn}')
            """)