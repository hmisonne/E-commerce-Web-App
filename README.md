# E-Commerce Web App Using Python Flask and SQLAlchemy.

Description
------------

After completing my first computer science class through CS50 (EDX), I decided to build an e-commerce website
using python, flask, SQLalchemy (and also HTML, CSS, Jinja).

The original website is hosted [here:](https://unwrapla.com/) and operated through Shopify. This is a zero waste business offering
refilling services for cleaning and beauty products.

I reproduced this web app and tried to imitate their design and main features. 

On this project I focused on implementing a shopping cart that uses a dynamic database. Once logged in, the user can browse products 
and add them or remove them from their cart.

The database includes 3 models: User, Products and Cart. When a user add a product to his cart, a new "cart item" will be added
to the Cart model with the user id and product id. When the user click on his cart, he will be able to see what is in his cart
(product name, price) and remove an item from its cart.


Install
------------
To run this website on your computer, once you are in the unwrap folder (command prompt) enter 

`python run.py`

Contribution
------------

What else could be implemented:
- The option for an admin user to enter products (the products are currently loaded from a CSV file with the import function) 
- The option to check out


Resources
------------

- Corey Schafer youtube tutorial "Python Flask Tutorial: Full-Featured Web App"
https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

- Corey Schafer github repository
https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog

- Durgaprasad-Nagarkatte github repository
https://github.com/Durgaprasad-Nagarkatte/Simple-Flask-Shopping-Cart

- Flask/SQLAlchemy documentation
https://flask-sqlalchemy.palletsprojects.com/en/2.x/

- Bootstrap
https://getbootstrap.com/
