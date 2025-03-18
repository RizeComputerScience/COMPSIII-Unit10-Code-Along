from books_to_scrape import *

# Call your books_to_scrape function here and create your SQL commands here
import sqlite3

# Create a books database
connection = sqlite3.connect('books.db')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS books")
cursor.execute('''CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price REAL,
    rating INTEGER,
    availability TEXT,
    genre TEXT
    );
''')

# Scrape the fiction page
BASE_URL = "http://books.toscrape.com/catalogue/category/books/fiction_10/page-{}.html"

books = scrape_pages(BASE_URL, 1, 4)

# Insert the values into the books database
for book in books:
    cursor.execute('''
        INSERT INTO books (title, price, rating, availability, genre)
        VALUES (?, ?, ?, ?, ?)
    ''', (book[0], book[1], book[2], book[3], book[4]))

# Commit the values
connection.commit()

# Get the values to confirm it works
data = cursor.execute('SELECT * from books;')

for book in data:
    print(book)