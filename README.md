#Shopping List API
Project description
Brief highlights about the following concepts is necessary:

API
REST
JSON

An API, acronym for Application Programming Interface, provides a blueprint for how software programs interacts with each other.

REST

REST is an acronym that stands for REpresentational State Transfer and has become the de-facto way of building API's and thus API's using this standard are known as RESTFul API's. The five main principles the implementation of REST and RESTFulness are:

Everything is a resource.
Every resource has a unique identifier.
Use simple and uniform interfaces.
Communication is done by representation.
Aim to be Stateless.
JSON

Yet another acronym, JSON which stands for Javascript Object Notation, is a light-weight format that facilitates interchange of data between different systems or, case in point, software. It is intended to be universal and thus allows consumption of data by any program regardless of the programming language it is written in. Sample JSON data would be as follows:

{
    "name":"John Does",
    "email":"johndoe@gmail.com",
}

Installation

Clone the GitHub repo:

http:

$ git clone https://github.com/JoyLubega/ShoppingListAPI
cd into the folder and install a virtual environment

$ virtualenv venv

Activate the virtual environment

$ . venv/bin/activate

Install all app requirements

$ pip install -r requirements.txt Create the database and run migrations

$ createdb flask_api

$ createdb testing_db

$ python manage.py db init

$ python manage.py db migrate

$ python manage.py db upgrade

All done! Now, start your server by running python manage.py runserver. You could use a GUI platform like postman to make requests to and fro the api.
