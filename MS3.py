import requests
from bs4 import BeautifulSoup

# Base URL of the site
base_url = 'https://books.toscrape.com/'

# Function to get the soup object
def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return BeautifulSoup(response.text, 'html.parser')

# Function to get the URL of the Romance category
def get_romance_category_url(base_url):
    soup = get_soup(base_url)
    category_link = soup.find('a', href=lambda x: x and 'category/books/romance_' in x)
    return base_url + category_link['href']

# Function to extract all books and links from the Romance category
def get_books_from_category(category_url):
    books = []
    while True:
        soup = get_soup(category_url)
        # Find all books
        book_items = soup.find_all('h3')
        for item in book_items:
            book_title = item.find('a')['title']
            book_url = base_url + item.find('a')['href'].replace('../../../', '')
            books.append((book_title, book_url))

        # Check for a "next" button to handle pagination
        next_button = soup.find('li', class_='next')
        if next_button:
            next_link = next_button.find('a')['href']
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_link
        else:
            break
    return books

# URL of the website
url = 'https://books.toscrape.com/'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the nav list (it's within a <div> tag with the class 'nav-list')
    nav_list = soup.find('ul', class_='nav nav-list')
    
    # Print the nav-list content
    print(nav_list.prettify())
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Main function
def main():
    # Get the Romance category URL
    romance_url = get_romance_category_url(base_url)
    print(f"Romance category URL: {romance_url}")

    # Get all books and links from the Romance category
    books = get_books_from_category(romance_url)

    # Print all books and their links
    for title, link in books:
        print(f"Title: {title}\nLink: {link}\n")

# Call the main function
if __name__ == "__main__":
    main()



