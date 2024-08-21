# Download all books, categories and images
import os
import requests
from bs4 import BeautifulSoup
import csv
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

base_url = "https://books.toscrape.com/"
url = f"{base_url}index.html"

# Fetch the HTML content
response = requests.get(url)
response.raise_for_status()

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Finding navigation list
nav_list = soup.find('ul', class_="nav nav-list")
categories = nav_list.find_all('a')[1:] 

def extract_book_details(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table table-striped')

    upc = table.find('th', text='UPC').find_next('td').get_text(strip=True)
    product_type = table.find('th', text='Product Type').find_next('td').get_text(strip=True)
    price = table.find('th', text='Price (incl. tax)').find_next('td').get_text(strip=True)
    tax = table.find('th', text='Tax').find_next('td').get_text(strip=True)
    availability = table.find('th', text='Availability').find_next('td').get_text(strip=True)
    num_reviews = table.find('th', text='Number of reviews').find_next('td').get_text(strip=True)
    
    # Find the image URL
    image_url = base_url + soup.find('img')['src'].replace('../../', '')
    
    return {
        'UPC': upc,
        'Product Type': product_type,
        'Price': price,
        'Tax': tax,
        'Availability': availability,
        'Number of Reviews': num_reviews,
        'Image URL': image_url
    }

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Category', 'Book Title', 'UPC', 'Product Type', 'Price', 'Tax', 'Availability', 'Number of Reviews', 'Image Path'])
        for book in data:
            csv_writer.writerow([
                book['Category'], book['Title'], book['UPC'], book['Product Type'], 
                book['Price'], book['Tax'], book['Availability'], book['Number of Reviews'], book['Image Path']
            ])

all_books_data = []
images_folder = 'book_images'

# Create a folder for images if it doesn't exist
os.makedirs(images_folder, exist_ok=True)

for category in categories:
    category_name = category.get_text(strip=True)
    category_url = base_url + category['href']
    print(f'Category: {category_name} - URL: {category_url}')
    page_number = 1

    while True:
        # Handle first page URL
        if page_number == 1:
            url = category_url
        else:
            url = f"{category_url.replace('index.html', '')}page-{page_number}.html"
        
        response = requests.get(url)
        if response.status_code != 200:
            break  # Exit the loop if no more pages are found

        category_soup = BeautifulSoup(response.content, 'html.parser')
        books = category_soup.find_all('article', class_='product_pod')

        if not books:
            break  # Exit loop if no books are found (end of pagination)

        # Iterate through each book to extract details
        for book in books:
            book_title = book.h3.a['title']
            book_url = base_url + 'catalogue/' + book.h3.a['href'].replace('../../../', '')
            book_details = extract_book_details(book_url)
            book_data = {
                'Category': category_name,
                'Title': book_title,
                'UPC': book_details['UPC'],
                'Product Type': book_details['Product Type'],
                'Price': book_details['Price'],
                'Tax': book_details['Tax'],
                'Availability': book_details['Availability'],
                'Number of Reviews': book_details['Number of Reviews'],
            }
            
            # Determine the local file path to save the image
            image_filename = f"{book_details['UPC']}.jpg"
            image_path = os.path.join(images_folder, image_filename)
            
            # Download the book's image
            download_image(book_details['Image URL'], image_path)
            
            # Add the image path to the book data
            book_data['Image Path'] = image_path

            all_books_data.append(book_data)

        page_number += 1

# Save all book data to CSV
save_to_csv(all_books_data, "BooksList.csv")

print("Scraping completed, data saved to BooksList.csv, and images downloaded.")

# Download csv with all books and all categories
# import requests
# from bs4 import BeautifulSoup
# import csv
# import warnings

# warnings.filterwarnings("ignore", category=DeprecationWarning)

# base_url = "https://books.toscrape.com/"
# url = f"{base_url}index.html"

# # Fetch the HTML content
# response = requests.get(url)
# response.raise_for_status()

# # Parse the HTML content
# soup = BeautifulSoup(response.content, 'html.parser')

# # Find the navigation list
# nav_list = soup.find('ul', class_="nav nav-list")
# categories = nav_list.find_all('a')[1:]  # Skip the first 'Books' category

# def extract_book_details(book_url):
#     response = requests.get(book_url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     table = soup.find('table', class_='table table-striped')

#     upc = table.find('th', text='UPC').find_next('td').get_text(strip=True)
#     product_type = table.find('th', text='Product Type').find_next('td').get_text(strip=True)
#     price = table.find('th', text='Price (incl. tax)').find_next('td').get_text(strip=True)
#     tax = table.find('th', text='Tax').find_next('td').get_text(strip=True)
#     availability = table.find('th', text='Availability').find_next('td').get_text(strip=True)
#     num_reviews = table.find('th', text='Number of reviews').find_next('td').get_text(strip=True)

#     return {
#         'UPC': upc,
#         'Product Type': product_type,
#         'Price': price,
#         'Tax': tax,
#         'Availability': availability,
#         'Number of Reviews': num_reviews
#     }

# def save_to_csv(data, filename):
#     with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(['Category', 'Book Title', 'UPC', 'Product Type', 'Price', 'Tax', 'Availability', 'Number of Reviews'])
#         for book in data:
#             csv_writer.writerow([
#                 book['Category'], book['Title'], book['UPC'], book['Product Type'], 
#                 book['Price'], book['Tax'], book['Availability'], book['Number of Reviews']
#             ])

# all_books_data = []

# for category in categories:
#     category_name = category.get_text(strip=True)
#     category_url = base_url + category['href']
#     print(f'Category: {category_name} - URL: {category_url}')
#     page_number = 1

#     while True:
#         # Handle first page URL
#         if page_number == 1:
#             url = category_url
#         else:
#             url = f"{category_url.replace('index.html', '')}page-{page_number}.html"
        
#         response = requests.get(url)
#         if response.status_code != 200:
#             break  # Exit the loop if no more pages are found

#         category_soup = BeautifulSoup(response.content, 'html.parser')
#         books = category_soup.find_all('article', class_='product_pod')

#         if not books:
#             break  # Exit loop if no books are found (end of pagination)

#         # Iterate through each book to extract details
#         for book in books:
#             book_title = book.h3.a['title']
#             book_url = base_url + 'catalogue/' + book.h3.a['href'].replace('../../../', '')
#             book_details = extract_book_details(book_url)
#             book_data = {
#                 'Category': category_name,
#                 'Title': book_title,
#                 'UPC': book_details['UPC'],
#                 'Product Type': book_details['Product Type'],
#                 'Price': book_details['Price'],
#                 'Tax': book_details['Tax'],
#                 'Availability': book_details['Availability'],
#                 'Number of Reviews': book_details['Number of Reviews']
#             }
#             all_books_data.append(book_data)

#         page_number += 1

# # Save all book data to CSV
# save_to_csv(all_books_data, "BooksList.csv")

# print("Scraping completed and data saved to BooksList.csv")
