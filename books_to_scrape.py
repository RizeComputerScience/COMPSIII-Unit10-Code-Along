# Create your books_to_scrape function here
import requests
from bs4 import BeautifulSoup
import re
from word2number import w2n

def scrape_pages(url, start, end):
    books = []
    genre_match = re.search(r'/category/books/([^_]+)_', url)
    genre = genre_match.group(1).title()
    

    for page in range(start, end + 1):
        response = requests.get(url.format(page))
        webpage = BeautifulSoup(response.content, 'html.parser')
        book_elements = webpage.find_all('article', class_='product_pod')
        # Get the title, price, availability, rating
        for book in book_elements:
            title = book.h3.a['title']
            price = float(book.find('p', class_='price_color').text.strip('£'))
            availability = book.find('p', class_='instock availability').text.strip()
            rating = w2n.word_to_num(book.find('p', class_ = "star-rating")['class'][1])
            books.append([title, price, availability, rating, genre])






    return books