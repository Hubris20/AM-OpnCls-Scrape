This notebook includes data scraping of books.toscrape.com

It extracts the information by using the steps below

Using beautiful soup, it parses the html content
Inspecting the html, it creates a dynamic url to retrieve the requested data
After finding the categories by using the navigation list, it extracts the data for each book in each page
Included in the book data is Title, UPC, Product Type, Price, Tax, Availability (including inventory), Number of Reviews, and the Book Image
Once it extracts the data, it sorts by category, and then saves all the data to a CSV file, with the images saved to a folder on the localized database


To run the application code, you will have to develop a virtual environment

To set up a virtual environment (for windows): 
1. You will have to install virtual environment using:
       a. pip install virtualenv
2. You will have to locate the repo code using cd and ls functions to find it after you downloaded it from the github
3. for me, i needed to change the execution policy to be able to run the virtual environment script by running the following:
       a. Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
4. This made it possible for me to activate the virtual environment by running the following:
       a. myenv\Scripts\Activate
5. Once the virtual environment is activated, you will see the added (myenv) text to the prompt from this point on
6. with the virtual environment activated, you can now run the following before initiating the code:
       a. pip install -r requirements.txt
7. Once the requirements has downloaded, you can now run the application code by entering:
       a. python Malevic_Asmir_1_repo_082024.py
8. This should run the application. Once it is all completed, to exit the virtual environment, don't forget to enter the following:
       a. deactivate
