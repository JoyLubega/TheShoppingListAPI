
[![Namuli Joyce](https://img.shields.io/badge/Namuli-Joyce-green.svg)]()
[![Coverage Status](https://coveralls.io/repos/github/JoyLubega/TheShoppingListAPI/badge.svg?branch=develop)](https://coveralls.io/github/JoyLubega/TheShoppingListAPI?branch=develop)
[![Build Status](https://travis-ci.org/JoyLubega/TheShoppingListAPI.svg?branch=develop)](https://travis-ci.org/JoyLubega/TheShoppingListAPI)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

# SHOPPINGLIST API

The innovative Shoppinglist app is an application that allows users  to record things they want to Buy  This is the backend API for enabling users to perform crud operations on shoppinglist and items with user persistence.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
- Just clone this repository by typing: `https://github.com/JoyLubega/TheShoppingListAPI.git`
- Switch to project directory: `cd TheShoppingListAPI`
- Install project requirements using python pip. But wait, you have to have some stuff before you get to this point. So these are:

### Prerequisites

- Python3.6 and above
- Python virtual environment
Just type:
```
python -V
```
in your terminal and if its not greater than or equal to 3.6, you're not in big trouble, there are tons of tutorials to get up up and running with these. Just grub one then come back when done.

### Installing

Now, you have python3 and a way of running a virtual environment. Lets set up the project environment.(remember we're still in the app directory)

1. Create your virtual environment. Usually, without any wrappers:
```
python -m venv my_venv
```
2. Start your virtual environment:
```
source my_venv/bin/activate
```
3. Install the project requirements specified in the requirements.txt file. Usually,
```
pip install -r requirements.txt
```
4. *Do Migrations*. This application uses postgresql. If you don't have psql you may install it here.
Create a `flask_api` database to be used by the application while running on your localhost.
Then, you can do migrations as:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

This is enough to get you started.
You can now run the application using:

`python run.py`

    
## Running the testsz

Easy, just: `nosetests`

## API Endpoints
You can use postman or even curl to reach out to the following api endpoints:

URL Endpoint	|               HTTP Request   | Resource Accessed | Access Type|
----------------|-----------------|-------------|------------------
/auth/register   |      POST	| Register a new user|publc
/auth/login	  |     POST	| Login and retrieve token|public
/auth/logout	  |     POST	| Logout and thus deactivate token|public
/auth/reset-password	  |     PUT	| Reset your password when logged in|private
/shoppinglists	              |      POST	|Create a new shoppinglist|private
/shoppinglists	              |      GET	|     Retrieve all shoppinglist for user|private
/shoppinglists/<shoppinglist_id>            |  	GET	    | Retrieve a shoppinglist by ID | private
/shoppinglists/<shoppinglist_id>	          |      PUT	|     Update a shoppinglist |private
/shoppinglists/<shoppinglist_id>	          |      DELETE	| Delete a shoppinglist |private
/shoppinglists/<shoppinglist_id>/items/  |           GET    |Retrive items in a given shoppinglist|private
/shoppinglists/<shoppinglist_id>/items/     |     POST	| Create items in a shoppinglist |private
/shoppinglists/<shoppinglist_id>/items/<item_id>|	DELETE	| Delete an item in a shoppinglis |prvate
/shoppinglists/<shoppinglist_id>/items/<item_id>|	PUT   	|update a shoppinglis item details |priate



## Built With

* [Python Flask](https://www.fullstackpython.com/flask.html) - The web framework used for this API

## Contributing

You can create your pull request. :D




## License

This project is currently under the [Creative Commons](https://creativecommons.org/) attribution.

## Acknowledgments

* Andela  - Inspiring the idea.