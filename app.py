# sudo myenv/bin/python3 app.py

import sqlite3
import sqlite3
from flask import Flask, jsonify, render_template, request, url_for, redirect, make_response
from Xenia.led import flashLED_async, clearLEDs_async
from motor_control import move_async
import numpy as np


if __name__ == "__main__":
    con = sqlite3.connect("books.db", check_same_thread=False)
    cur = con.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS books(
            title VARCHAR,
            author VARCHAR,
            year INTEGER,
            genre VARCHAR,
            isbn VARCHAR,
            row INTEGER,
            position FLOAT,
            width FLOAT
        )"""
    )        


app = Flask(__name__)

#Startseite
@app.route('/')
def index():
    clearLEDs_async()
    return render_template('index.html')


#Bücher hinzufügen
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    #prüfen, ob Buch schon existiert
    alreadyexists = request.args.get('alreadyexists', None)
    return render_template('add_book.html', alreadyexists=alreadyexists)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    genre = request.form.get('genre')
    isbn = request.form.get('isbn')
    row = request.form.get('row')
    position = request.form.get('position')
    width = request.form.get('width')

    # check if book already exists
    book = cur.execute(f"SELECT * FROM books WHERE isbn = '{isbn}'").fetchone()
    if book:
        return redirect(url_for('add_book', alreadyexists=True))

    cur.execute(f"""
                INSERT INTO books (title, author, year, genre, isbn, row, position, width) VALUES
                ('{title}', '{author}', {year}, '{genre}', '{isbn}', {row}, {position}, {width})
            """)
        
    con.commit()
    return redirect(url_for('show_books', isbn=isbn))


#Bücher suchen
@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    #Fehlermeldung, falls Buch nicht vorhanden
    nobook = request.args.get('nobook', None)
    return render_template('search_book.html', nobook=nobook)


#Bücher anzeigen
@app.route('/show_books', methods=['GET'])
def show_books():
    #clearLEDs_async()
    print(request.args)
    search = request.args.get('search', None)
    sort_by = request.args.get('sorting', 'title')  # Defaultwert der Sortierung ist Titel
    title = request.args.get('title', None)
    isbn = request.args.get('isbn', None)
    author = request.args.get('author', None)
    genre = request.args.get('genre', None)
    
    query = "SELECT * FROM books "
    all_books = True

    if isbn:
        query = query + f"WHERE isbn = '{isbn}' "
        all_books = False
    elif title:
        query = query + f"WHERE title LIKE '%{title}%' "
        all_books = False
    elif author:
        query = query + f"WHERE author LIKE '%{author}%' "
        all_books = False
    elif genre:
        query = query + f"WHERE genre LIKE '%{genre}%' "
        all_books = False

    if sort_by == 'author':
        query = query + "ORDER BY author ASC"
    elif sort_by == 'position':
        query = query + "ORDER BY row ASC, position ASC"
    elif sort_by == 'yearNew':
        query = query + "ORDER BY year DESC"
    elif sort_by == 'yearOld':
        query = query + "ORDER BY year ASC"
    else:  # Default
        query = query + "ORDER BY title ASC"

    books = cur.execute(query).fetchall()

    if not books and not all_books:
        return redirect(url_for('search_book', nobook=True))
    
    if all_books:
        clearLEDs_async()
    else:
        # Aufrufen der LED-Funktion mit Positionen und Breiten der gefundenen Bücher
        positions = np.array(list([book[6]] for book in books))  # Jede Position wird zu einer Liste
        widths = np.array(list([book[7]] for book in books))     # Jede Breite wird zu einer Liste
        flashLED_async(positions, widths)
        book_center = positions + 0.5*widths
        if search:
            move_async(book_center, 50)

    


    return render_template('show_books.html', books=books, all_books=all_books, search=search)


#Buch löschen
@app.route('/delete', methods=['POST'])
def delete():
    clearLEDs_async()
    isbn = request.form.get('isbn')
    if isbn:
        cur.execute(f"DELETE FROM books WHERE isbn = '{isbn}'")
        con.commit()
    return redirect(url_for('show_books'))


#Buch bearbeiten
@app.route('/edit_book/<isbn>', methods=['GET', 'POST'])
def edit_book(isbn):
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')
        genre = request.form.get('genre')
        row = request.form.get('row')
        position = request.form.get('position')
        width = request.form.get('width')

        # Update the book in the database
        cur.execute("""
            UPDATE books
            SET title = ?, author = ?, year = ?, genre = ?, row = ?, position = ?, width = ?
            WHERE isbn = ?
        """, (title, author, year, genre, row, position, isbn, width))

        con.commit()
        return redirect(url_for('show_books'))

    #Aktuelle Buchdetails abrufen
    book = cur.execute("SELECT * FROM books WHERE isbn = ?", (isbn,)).fetchone()

    if book:
        # LED für das Buch aufleuchten lassen
        flashLED_async([[book[6]]], [[book[7]]])  # Position und Breite an die LED-Funktion übergeben

    return render_template('edit_book.html', book=book)


if __name__ == "__main__":
    app.run(debug=True, threaded=False, host='0.0.0.0') # App ist von jedem Gerät im Netzwerk erreichbar