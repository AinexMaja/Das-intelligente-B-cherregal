import duckdb
from button_click import handle_button_click

def create_database(database):
    # Datenbank und Tabelle erstellen, wenn sie nicht existierts
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

    # # ('title', 'author', year, 'genre', width, height, depth, row, position, 'isbn')
    # database.execute('''
    # INSERT INTO books (title, author, year, genre, width, height, depth, row, position, isbn) VALUES
    # ('Alles überall auf einmal', 'Miriam Meckel; Léa Steinacker', 2024, 'Technologie', 3.16, 20.9, 12.9, 1, 0, '3498007106'),
    
    # ('Das Hohe Haus', 'Roger Willemsen', 2015, 'Politik', 3.13, 19, 12.5, 1, 6.7, '3596198100'),
    # ('Die Schule meines Lebens', 'Matze Hielscher', 2020, 'Interviews', 2.75, 20.5, 13.6, 1, 10.2, '3492062180'),
    # ('If Then', 'Jill Lepore', 2020, 'Science', 3.81, 24.38, 16.26, 1, 13.1, '1631496107'),
    # ('Im Grunde gut', 'Rutger Bregman', 2021, 'Philosophie', 3.04, 12.5, 19, 1, 16.5, '349900416X'),
    # ('How to', 'Randall Munroe', 2019, 'Science', 3.3, 21.6, 13.6, 1, 19.8, '3328600914')
                     
    # ''')
    # # ('Nerds', 'Sibylle Berg', 2020, 'Interviews', 3.1, 21, 12.8, 1, 3.4, '3462054600')