# E-Commerce Test Store

## Description

This is a simple e-commerce store built with Django and Celery. It uses the following technologies:

- Django
- Celery
- Redis
- PostgreSQL
- Docker

It's a simple e-commerce store that:

1. allows users to browse products that are organized into categories of unlimited depth
2. allows users to add products to their cart
3. allows users to complete their cart and checkout
4. allows users to sign up and login using Google OAuth2

Additionally, it supports REST APIs for:

1. create products
2. get the average price for products in a particular category
3. has APIs that take the customer through the entire checkout process
4. authentication is done via Django's built-in `SessionAuthentication` backend

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository
2. Run `bin/start` or `docker compose up -d` to start the containers
3. Run `docker compose exec app python manage.py migrate` to create the database tables
4. Run `docker compose exec app python manage.py createsuperuser` to create a superuser

### Running the application

1. Open your browser and navigate to `<http://localhost:5000/admin>
2. Login with the superuser credentials
3. Navigate to the Categories page and create some categories
4. Navigate to the Products page and create some products
5. Log out and go to the home page
6. Click on the "Login with Google" button
7. Log in with your Google account
8. After logging in, you should be redirected to a form where you can fill out your phone number
9. After submitting the form, you should be redirected to the home page.
10. Add some products to your cart and click on the "Cart" button
11. You should be redirected to the checkout page
12. You can either complete the checkout process or click on the "Clear Cart" button
13. You should be redirected to the profile page
