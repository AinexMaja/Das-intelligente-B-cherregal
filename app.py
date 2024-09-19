import sqlite3
import sqlite3
from flask import Flask, jsonify, render_template, request, url_for, redirect, make_response
#from led import flashLED_async, clearLEDs_async
#from motor_control import move_async
#import numpy as np


if __name__ == "__main__":
    # Connect to the SQLite database
    con = sqlite3.connect("books.db", check_same_thread=False)
    cur = con.cursor()

    # Create the 'books' table if it doesn't exist
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

# Initialize the Flask application
app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    clearLEDs_async()  # Turn off all LEDs when the homepage is accessed
    return render_template('index.html')


# Route to add a book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    # Check if the book already exists
    alreadyexists = request.args.get('alreadyexists', None)
    return render_template('add_book.html', alreadyexists=alreadyexists)

# Route to handle adding a book
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

    # Check if book already exists in the database
    book = cur.execute(f"SELECT * FROM books WHERE isbn = '{isbn}'").fetchone()
    if book:
        return redirect(url_for('add_book', alreadyexists=True))

    # Insert the new book into the database
    cur.execute(f"""
                INSERT INTO books (title, author, year, genre, isbn, row, position, width) VALUES
                ('{title}', '{author}', {year}, '{genre}', '{isbn}', {row}, {position}, {width})
            """)
        
    con.commit()
    return redirect(url_for('show_books', isbn=isbn))


# Route to search for a book
@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    # Display error message if no book is found
    nobook = request.args.get('nobook', None)
    return render_template('search_book.html', nobook=nobook)


# Route to display books
@app.route('/show_books', methods=['GET'])
def show_books():
    #clearLEDs_async()  # Turn off all LEDs when the show_books is accessed
    search = request.args.get('search', None)
    sort_by = request.args.get('sorting', 'title')   # Default sorting by title
    title = request.args.get('title', None)
    isbn = request.args.get('isbn', None)
    author = request.args.get('author', None)
    genre = request.args.get('genre', None)
    
    query = "SELECT * FROM books "
    all_books = True

    # Build query based on search parameters
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

    # Add sorting to the query
    if sort_by == 'author':
        query = query + "ORDER BY author ASC"
    elif sort_by == 'position':
        query = query + "ORDER BY row ASC, position ASC"
    elif sort_by == 'yearNew':
        query = query + "ORDER BY year DESC"
    elif sort_by == 'yearOld':
        query = query + "ORDER BY year ASC"
    else:  # Default sorting by query
        query = query + "ORDER BY title ASC"

    books = cur.execute(query).fetchall()

    # Redirect to search page if no books are found and not all books were requested
    if not books and not all_books:
        return redirect(url_for('search_book', nobook=True))
    
    if all_books:
        clearLEDs_async()  # Turn off all LEDs when showing all books
    else:
        # Calling the LED function with positions and widths of the books found
        positions = np.array(list([book[6]] for book in books))  # Each position as a list
        widths = np.array(list([book[7]] for book in books))     # Each width as a list
        flashLED_async(positions, widths)
        # Calculate center of each book
        book_center = positions + 0.5*widths
        if search:
            move_async(book_center, 50)  # Move motor to center of the books if searching

    return render_template('show_books.html', books=books, all_books=all_books, search=search)


# Route to delete a book
@app.route('/delete_book', methods=['POST'])
def delete():
    clearLEDs_async()  # Turn off all LEDs before deleting
    isbn = request.form.get('isbn')
    if isbn:
        cur.execute(f"DELETE FROM books WHERE isbn = '{isbn}'")
        con.commit()
    return redirect(url_for('show_books'))


# Route to edit a book
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

        # Update the book details in the database
        cur.execute("""
            UPDATE books
            SET title = ?, author = ?, year = ?, genre = ?, row = ?, position = ?, width = ?
            WHERE isbn = ?
        """, (title, author, year, genre, row, position, width, isbn))

        con.commit()
        return redirect(url_for('show_books'))

    # Fetch current book details for editing
    book = cur.execute("SELECT * FROM books WHERE isbn = ?", (isbn,)).fetchone()

    if book:
        # Flash LED for the book being edited
        flashLED_async([[book[6]]], [[book[7]]])  # Call LED function with position and width

    return render_template('edit_book.html', book=book)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True, threaded=False, host='0.0.0.0')