import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

base_url = "https://books.toscrape.com/"

def scrape_category(category_url):
    all_book_data = []
    page = 1

    while True:
        url = f"{category_url}?page={page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        book_containers = soup.find_all('article', class_='product_pod')
        if not book_containers:
            break  # No more books

        for book in book_containers:
            book_url = urljoin(base_url, book.h3.a['href'])
            book_data = scrape_book_details(book_url)
            all_book_data.append(book_data)

        next_page_link = soup.find('li', class_='next')
        if not next_page_link:
            break  # No next page

        page += 1

    return all_book_data

def scrape_book_details(book_url):
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the product information table
    table = soup.find('table', class_='product_info')

    # Extract data from table rows
    data = {}
    for row in table.find_all('tr'):
        key = row.th.text.strip()
        value = row.td.text.strip()
        data[key] = value

    # Extract additional information
    title = soup.find('h1').text
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].a.text
    upc = data['UPC']
    product_type = data['Product Type']
    price = soup.find('p', class_='price_color').text.strip()
    tax = data['Tax']
    availability = data['Availability']
    quantity_available = int(availability.split('(')[-1].split(' ')[0])
    number_of_reviews = int(soup.find('p', class_='star-rating').next_sibling.strip())

    return {
        'Category': category,
        'Book Title': title,
        'UPC': upc,
        'Product Type': product_type,
        'Price': price,
        'Tax': tax,
        'Availability': availability,
        'Quantity Available': quantity_available,
        'Number of Reviews': number_of_reviews
    }


def scrape_category(category_url):
    response = requests.get(category_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')


    book_containers = soup.find_all('article', class_='product_pod')
    book_titles = [book.h3.a['title'] for book in book_containers]
    return book_titles

def main():
    url = f"{base_url}index.html"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    nav_list = soup.find('ul', class_=["nav", "nav-list"])
    category_urls = []
    for item in nav_list.find_all('li'):
        link = item.find('a', href=True)
        if link:
            category_url = f"{base_url}{link['href']}"
            category_urls.append(category_url)

    for category_url in category_urls:
        book_titles = scrape_category(category_url)
        print(f"Category: {category_url}")
        print(book_titles)
        print()
    all_books = []
    for category_url in category_urls:
        category_books = scrape_category(category_url)
        all_books.extend(category_books)  

# Write data to CSV
    with open('listbooks.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Category', 'Book Title', 'UPC', 'Product Type', 'Price', 'Tax', 'Availability', 'Quantity Available', 'Number of Reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_books)

if __name__ == "__main__":
    main()