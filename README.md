# Nexxera Project 

### Objective

The goal of this project is to create an account with credit/debit and statement functions using the Python/Django RestFramework.

### Instructions 

In order to run the program please access the Terminal and go to the folder where the repository is saved and run the following commands 

* python manage.py makemigration 
* python manage.py migrate 
* python manage.py runserver

Then use the address provided by the terminal as the base url for the api. In my case it was "http://127.0.0.1:8000".

Proceed to the browser and use the following endpoints to perform operations 

* **http://127.0.0.1:8000/api/v1/accounts**: crud operations for accounts
* **http://127.0.0.1:8000/api/v1/transactions**: crud operations for transactions
* **http://127.0.0.1:8000/api/v1/statement**: filters transactions to display transactions and balances in different periods and by transaction types

