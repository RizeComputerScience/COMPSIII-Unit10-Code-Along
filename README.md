# COMPS III: Unit 10 Code Along

## Overview

Over the next 2 units, we’ll be scraping, cleaning, storing, and visualizing data from the website [Books to Scrape](https://books.toscrape.com/). This website contains a lot of sample scraping data that will allow us to practice all the skills that we will be learning.

This week, we’ll be be building functionality to:
- Scrape data from the website.
- Clean the data using regular expressions.
- Storing the data in a database.

By the end of this code along, you will have data that is processed and ready to be analyzed when we work with Python data analysis tools next week!

## Local Terminal
1. In your terminal, install the `beautifulsoup4`, `requests`, and `re` modules.

```bash
pip install beautifulsoup4 requests re
```

## VS Code - `books_to_scrape.py`

2. At the top of the `books_to_scrape.py`, import these modules at the top of the file along with the sqlite3 module.
```python
import requests 
from bs4 import BeautifulSoup 
import sqlite3 
import re
```
3. Define a function called `scrape_pages(url, start, end)`. The parameters for this function are:
    - `url`: The url to send the `GET` request to. The url has the following format `http://books.toscrape.com/catalogue/category/books/fiction_10/page-{}.html`. The `{}` indicate the place where the page will be placed
    - `start`: The first page to scrap
    - `end`: The last page to scrap
4. Create an empty list called `books` that will hold all the books that are scraped. This will be the value returned at the end of the function.

## VS Code - `main.py`

5. In `main.py`, call the function with the Books to Scrape website. To see the output as you progress through the remaining steps, simply run `python main.py` in your terminal.
```python
BASE_URL = "http://books.toscrape.com/catalogue/category/books/fiction_10/page-{}.html"
books = scrape_pages(BASE_URL, 1, 4)
```
6. Run the tests! `test_scrape_books_returns_list` test should now be passing.

## VS Code - `books_to_scrape.py`

7. Iterate through pages from `start` through `end`. Send a `GET` request to each page. Store the response in a variable called `response`. Print out the response to see what is returned.
8. For the content that was returned in the `response`, pass the content to the `BeautifulSoup` method and save the value in a variable. Print out the result.
9. Each book is contained within an `<article>` HTML element with a class of `product_pod`. Call `.find_all()` on the webpage variable. Save the value that is returned in a variable. This will give you a list of article elements.
10. Finally, iterate through the variable that contains your article elements. Extract the title, price, and availability. Add these values as a list to your books variable that your function will return.
    - **NOTE**: We will handle genre and rating in the next section as they require additional formatting!

## VS Code - `books_to_scrape.py`
11. The genre of the book is in the url with the format `.../category/books/fiction_10/....`  The regex to extract fiction would look like `r'/category/books/([\w-]+)_\d+/'`
12. Inside the `scrape_pages` function, use the `re.search()` method to extract the genre from the url.
13. Call `.group(1)` on the returned Match object since we only want the capturing group, not the full string that contains /category/books.
def scrape_pages(url, start, end):
14. Update the returned books list to include the `genre`.
15. The data that we extracted has some issues and needs to be cleaned before we can store it to our SQL database. The following issues are currently present:
    - The `genre` is lowercase and should be capitalized like a title.
    - The `availability` has some additional whitespace that needs to be removed.
    - The `price` has a currency character and needs to be converted to a float.
    - The `rating` is a string of the star rating, but should be an integer.
Let’s clean this data!
16. Call `.title()` on the `genre` in order to capitalize the first letter in the string.
17. Call `.strip()` on the `availability` in order to remove the whitespace.
18. Call `.strip()` on the price and pass in ‘£’ in order to remove the currency character. Wrap this in a `float()` to convert this to a float.
19. Since the ratings are always the word version of the number (e.g. ‘One’ instead of 1), we use the word2number module. First, you should install `word2number` in your terminal with `pip install word2number`.
20. Import w2n from word2number at the top of the file 
21. Finally, pass the returned string for `rating` to the `w2n.word_to_num()` method. 

## VS Code - `main.py`
22. Run the function and print out the returned value. Verify that the list values have been properly cleaned. The result should look similar to the structure below
```bash
[['Soumission', 50.1, 1, 'In stock', 'Fiction'], ['Private Paris (Private #10)', 47.61, 5, 'In stock', 'Fiction'], ... ]
```
23. Run the tests! `test_scrape_books_genre` should now be passing.
24. The data now needs to be inserted into a database. Create a file called books.db.
25. Import the sqlite3 module and create a books database with the correct columns and data types.
26. For the books that are returned from your `books_to_scrape` function call, iterate through the list and insert them into your database.
27. Run the tests! `test_books_table_exists`, `test_books_table_columns`, and `test_scrape_books_data_added` should now be passing.
28. Finally, print out the data that is stored in the database.