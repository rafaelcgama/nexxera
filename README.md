# Nexxera Project 

### Objective

The goal of this project is to create an account with credit/debit and statement functions using the Python/Django RestFramework.

### Instructions 

In order to run the program please access the Terminal and to the folder where the repo is located and execute the docker compose file after the virtual environment is created:  

* docker-compose up

Then use 0.0.0.0:8000 or localhost:8000 as base for the api endpoints and proceed to the browser to access them by using following urls:

* **localhost:8000/api/v1/accounts**: crud operations for accounts
* **localhost:8000/api/v1/transactions**: crud operations for transactions
* **localhost:8000/api/v1/statement**: filters transactions to display transactions and balances in different periods and by transaction types

PS: To add transactions, always use positive numbers for the amount. The app will add the sign automatically according to the transaction type selected.