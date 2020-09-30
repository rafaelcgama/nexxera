# Nexxera Project

## _Objective_

The goal of this project is to create an account with credit/debit and statement functions using the Python/Django RestFramework.

## _Instructions_

First, you must have Docker installed in your computer so if you don't have it already please go ahead and install it. Once you have Docker installed and running please access the Terminal, go to the folder where the repo is located and execute the docker compose file:

* docker-compose up

This API ins consisted of 3 endpoints with the following functionalities:

* **/accounts/**: perform curd operations for accounts
* **/transactions/**: perform crud operations for transactions
* **/statement/**: filters transactions to display transactions and balances in different periods and by transaction types


In order to use the program, an account (or more) must be created using the **account** endpoint. Once that's done, the transactions need to be insert via the **transaction**. Finally, the statements can be created using the **statement** endpoint using the dates of your choice.


### **Create an account**
To create an account please open your browser and access the **accounts** endpoint at:

* localhost:8000/api/v1/accounts

All fields must be entered in other to create the account



### **Add Transactions**

To add transaction please access the **transactions** endpoint at:

* localhost:8000/api/v1/transactions

All fields but the description must the added in order to create the transaction. Also, you must assign the transaction to one of the accounts that were created and only use positive numbers in the amount. The selection of debit or credit will select the correct sign internally.


### **Get Statements**

To create statements please access the **statement** endpoint at:

* localhost:8000/api/v1/statement

In order to get results, at least the account number must be entered. The other fields are optional and the user is free to selected them in whichever way he chooses to generate the desired statement.