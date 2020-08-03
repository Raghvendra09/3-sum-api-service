# 3-sum-api-service
This project contains following APIs
-  `api-token-auth` - Making `POST` request on this api with username and password in request body will get access token that should be used in other APIs with `Authorization` header.
-  `api/calculate-three-sum` - It takes a list and a sum in request body with method `POST` and return all combination of triplets with sum equal to given sum
-  `api/transaction-history` - Making `GET` request on this api will list all previous input and output data of above API.
 
 Project is implemented in Django (Django Rest Framework) and connected with Postgres database.
 
 # Steps to run on local
 - Create virtual enviornment by `virtualenv -p python3.6 venv`
 - Activate it by `source venv/bin/activate`
 - install requirements by `pip install -r requirements.txt`
 - Install postgres db, create database, add user and grant all privileges to the user as defined in `assignment/settings.py`
 - Run `python manage.py migrate` for db migration.
 - Run development server by `python manage.py runserver`
 - Create superuser by `python manage.py createsuperuser`
 - Obtain authentication token by using `api-token-auth` API.
