This notebook includes data scraping of books.toscrape.com

It extracts the information by using the steps below

Using beautiful soup, it parses the html content
Inspecting the html, it creates a dynamic url to retrieve the requested data
After finding the categories by using the navigation list, it extracts the data for each book in each page
Included in the book data is Title, UPC, Product Type, Price, Tax, Availability (including inventory), Number of Reviews, and the Book Image
Once it extracts the data, it sorts by category, and then saves all the data to a CSV file, with the images saved to a folder on the localized database
