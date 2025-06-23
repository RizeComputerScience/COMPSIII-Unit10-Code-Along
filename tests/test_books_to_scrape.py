import os
from books_to_scrape import *
import pytest
import sqlite3

@pytest.fixture
def db_connection():
    """Fixture to provide a database connection for tests"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'books.db')
    connection = sqlite3.connect(db_path)
    yield connection
    connection.close()

def test_scrape_books_returns_list():
    """Test that the function returns a list"""
    test_url = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
    start = 1
    end = 4
    result = scrape_pages(test_url, start, end)
    assert isinstance(result, list), "Function should return a list"
    assert len(result) > 0, "Function should return non-empty list"

# Test genre is extracted correctly and cleaned using regex
def test_scrape_books_genre():
    """Test that the genre is extracted correctly"""
    test_url = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
    start = 1
    end = 4
    result = scrape_pages(test_url, start, end)
    assert all(book[4] == "Fiction" for book in result), "Genre should be 'Fiction'"


# Test that the books table has been created
def test_books_table_exists(db_connection):
    """Verify that the users table exists in the database."""
    cursor = db_connection.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books';")
    result = cursor.fetchone()
    assert result is not None, "Books table does not exist"

# Test that the books table has the correct columns
def test_books_table_columns(db_connection):
    """Verify the schema of the books table."""
    cursor = db_connection.cursor()

    # Get table info
    cursor.execute("PRAGMA table_info(books);")
    columns = cursor.fetchall()
    
    # Expected columns and their types
    expected_columns = [
        ('id', 'INTEGER', 1, None, 1),  # Primary key, autoincrement
        ('title', 'TEXT', 0, None, 0),
        ('price', 'REAL', 0, None, 0),
        ('availability', 'TEXT', 0, None, 0),
        ('rating', 'INTEGER', 0, None, 0),
        ('genre', 'TEXT', 0, None, 0)
    ]
    
    # Check number of columns
    assert len(columns) == 6, f"Expected 6 columns, found {len(columns)}"
    
    # Check each column's details
    for expected, actual in zip(expected_columns, columns):
        assert actual[1] == expected[0], f"Column name mismatch: expected {expected[0]}, got {actual[1]}"
        assert actual[2] == expected[1], f"Column type mismatch for {actual[1]}"
        assert actual[5] == expected[4], f"Primary key configuration mismatch for {actual[1]}"
    
# Verify that data has been added to the books.db
def test_scrape_books_data_added(db_connection):
    """Test that data has been added to the books table"""
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM books")
    result = cursor.fetchall()
    assert len(result) > 0, "No data found in the books table"
    assert all(isinstance(row[0], int) for row in result), "ID should be an integer"
    assert all(isinstance(row[1], str) for row in result), "Title should be a string"
    assert all(isinstance(row[2], float) for row in result), "Price should be a float"
    assert all(isinstance(row[3], str) for row in result), "Availability should be a string"
    assert all(isinstance(row[4], int) for row in result), "Rating should be an integer"
    assert all(isinstance(row[5], str) for row in result), "Genre should be a string"
    assert all(row[5] == "Fiction" for row in result), "Genre should be 'Fiction'"