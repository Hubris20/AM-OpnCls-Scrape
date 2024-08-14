import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time


# Base URL of the website
url = 'https://books.toscrape.com/'

# Function to get soup object from a given URL
response = requests.get(url)
if response.status_code == 200:
    print("request successful")
else:
    print(f"request failed")
        

# create a soup object to parse the html
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
print(soup.prettify())

# find all books
books = soup.find_all('h3')

start_time = time.time()
books_extracted = 0

# Iterate information for each book

for book in books:
    book_url = book.find('a')['href']
    book_response = requests.get(url + book_url)
    book_soup = BeautifulSoup(book_response.content, "html.parser")

    title = book_soup.find('h1').text
    category = book_soup.find('ul', class_="breadcrumb").find_all('a')[2].text.strip()
    rating = book_soup.find('p', class_='star-rating')['class'][1]
    price = book_soup.find('p', class_='price_color').text.strip()
    availability = book_soup.find('p', class_='availability').text.strip()
    
    books_extracted +=1

    end_time = time.time()
    total_time = (end_time-start_time)/60.0

    print(f'Title: {title}')
    print(f'Category: {category}')
    print(f'Rating: {rating}')
    print(f'Price: {price}')
    print(f'Availability: {availability}')
    print('*******')


# Looping through 50 Pages of books

books_data=[]

for page_num in range (1,51): 
    url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')

    books_data.append({title, category, rating, price, availability})
    print(books_data)
    print('*******')
    print(f'Total time take: {total_time:.2f} minutes')
    print('*******')
    print(f'{page_num * len(books)} books extracted so far...')

    # Export the Data
    df = pd.DataFrame(books_data, columns=["Title", "Category", "Rating", "Price", "Availability"])

    # Display first 10 rows
    print(df.head(10))

    # save to CSV 
    df.to_csv("books_scraped.csv", index=False)
    print("Data saved to Books")



