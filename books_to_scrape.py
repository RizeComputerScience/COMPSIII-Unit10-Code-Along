# Create your books_to_scrape function here
# Import the requests, BeautifulSoup, sqlite3, and re modules
import requests
from bs4 import BeautifulSoup
import re
from word2number import w2n

# Create a scrap_page function that will scrape the Books to Scrape website
def scrape_pages(url, start, end):
    books = []
    # The genre is in the url. This looks for the /category/books raw string. 
    # ([\w]+) Captures the category name (letters, numbers, hyphens).
    # _ Matches the underscore character
    # \d+ matches one ore more digit
    # /index.html matches the literal text
    genre_match = re.search(r'/category/books/([\w-]+)_\d+/', url)
    # We use group(1) because we want just the capturing group (i.e. the think in ([\w]+) ), not the whole regex search.
    genre = genre_match.group(1).title()

    # iterate through pages 1 through 4 (the number of fiction pages that there are)
    for page in range(start, end + 1):
        response = requests.get(url.format(page))
        webpage = BeautifulSoup(response.content, 'html.parser')

        # Every book is in "article" element with a class of "product_pod".
        book_elements = webpage.find_all('article', class_='product_pod')
        # Iterate through all of these book elements and pull out the book information
        for book in book_elements:
            # Title is inside an h3 element. Note that some of the titles are incomplete but the anchor has the title as "title"
            title = book.h3.a['title']
            # Remove the currency and convert to float
            price = float(book.find('p', class_="price_color").text.strip('£'))
            # The rating class has the ratings for the book. The rating is stored as the second class name.
            # We use the word2number library to convert the rating to a number
            rating = w2n.word_to_num(book.find('p', class_='star-rating')['class'][1])
            # Get the availability and strip extra whitespace
            availability = book.find('p', class_='instock availability').text.strip()
            # Add all the content to the growing books list
            books.append([title, price, rating, availability, genre])
    print(books)
    return books