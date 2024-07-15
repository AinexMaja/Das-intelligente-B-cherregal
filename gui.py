import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QDialog
from PyQt5.QtCore import Qt  # Import des Qt-Moduls
import duckdb
from code.Buecherregal.led import LED2 as led

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.book_title = None

        self.setWindowTitle("Eingabe")
        self.resize(400, 200)

        layout = QVBoxLayout()  # Widgets werden vertikal angeordnet

        label = QLabel("Bitte gib den Titel des Buches ein:")
        label.setAlignment(Qt.AlignCenter)  # Text des Labels zentrieren
        layout.addWidget(label)

        self.textbox = QLineEdit()
        layout.addWidget(self.textbox)

        buttons_layout = QHBoxLayout()  # Buttons werden horizontal angeordnet

        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Abbrechen")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Bei "ok" Ausgabe des Buchtitels auf Konsole
        ok_button.clicked.connect(self.on_ok)

        # Bei "cancel" Abbruch
        cancel_button.clicked.connect(self.reject)

    def on_ok(self):
        self.book_title = self.textbox.text()
        self.accept()

def search_book():
    dialog = Dialog()
    if dialog.exec_() == QDialog.Accepted:
        book_title = dialog.book_title
        # Hier wird der Buchtitel zurückgegeben
        return book_title

def insert_book():
    dialog = Dialog()
    if dialog.exec_() == QDialog.Accepted:
        book_title = dialog.book_title
        # Hier wird der Buchtitel zurückgegeben
        return book_title

def main_window():
    w = QWidget()  # Objekt der QWidget Klasse erstellen
    w.resize(400, 200)
    w.setWindowTitle("Das intelligente Bücherregal")  # Das äußere Widget ist das Fenster

    main_layout = QVBoxLayout(w)  # Hauptlayout für das Fenster
    
    label = QLabel("Was möchtest Du tun?")
    label.setAlignment(Qt.AlignCenter)  # Text zentrieren
    main_layout.addWidget(label)

    hbox = QHBoxLayout()  # Layout für die Schaltflächen

    # Zwei Buttons erstellen
    btn1 = QPushButton("Nach Buch suchen")
    btn1.clicked.connect(lambda: handle_button_click('search'))
    hbox.addWidget(btn1)

    btn2 = QPushButton("Neues Buch hinzufügen")
    btn2.clicked.connect(lambda: handle_button_click('insert'))
    hbox.addWidget(btn2)

    main_layout.addLayout(hbox)

    return w

def handle_button_click(action):
    if action == 'search':
        book_title = search_book()
        if book_title:
            print(f"Gesuchter Buchtitel: {book_title}")
            result = database.sql(f"SELECT * FROM books WHERE title = '{book_title}'")
            position = database.execute(f"SELECT title, position FROM books WHERE title LIKE '%{book_title}%'")
            led(position)
            print(result)
    elif action == 'insert':
        book_title = insert_book()
        if book_title:
            print(f"Neuer Buchtitel: {book_title}")
            title = book_title
            author = None
            year = -1
            genre = None
            width = -1
            height = -1
            depth = -1
            row = -1
            position = -1
            isbn = None
            database.execute(f"""
                INSERT INTO books (title, author, year, genre, width, height, depth, row, position, isbn) VALUES
                ('{title}', '{author}', {year}, '{genre}', {width}, {height}, {depth}, {row}, {position}, '{isbn}')
            """)
def create_database():
    database.execute('''
    CREATE TABLE IF NOT EXISTS books (
        title VARCHAR,
        author VARCHAR,
        year INTEGER,
        genre VARCHAR,
        width FLOAT,
        height FLOAT,
        depth FLOAT,
        row INTEGER,
        position FLOAT,
        isbn VARCHAR
    )
    ''')

    # Optionally, insert some example data
    database.execute('''
    INSERT INTO books (title, author, year, genre, width, height, depth, row, position, isbn) VALUES
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Novel', 15.0, 22.0, 3.0, 1, 1.5, '1'),
    ('1984', 'George Orwell', 1949, 'Dystopian', 13.5, 21.5, 2.5, 2, 2.0, '2'),
    ('To Kill a Mockingbird', 'Harper Lee', 1960, 'Southern Gothic', 14.0, 23.0, 3.5, 3, 1.0, '3')
    ''')


    # Verify that the data has been inserted
    result = database.execute("SELECT * FROM books").fetchall()
    for row in result:
        print(row)
    print(database.sql("SELECT * FROM books"))

if __name__ == "__main__":
    database = duckdb.connect()
    create_database()

    app = QApplication(sys.argv)  # Objekt der QApplication Klasse erstellen
    w = main_window()
    w.show()
    sys.exit(app.exec_())
