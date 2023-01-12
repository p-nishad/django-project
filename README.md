# Homie!

**Homie!** is an E-commerce website  which sell home appliances.It allows you to search all products and buy by using Razorpay payment system

# Key Features

User registration and login wiht OTP verification.

Cart Functionality.

Search funtionality.

User profile and dashboard.

# Prerequisites

Python3

Django

Mysql or Postgresql

# Getting Started

## By cloning the repository

1. Clone the repo.
`git clone https://github.com/p-nishad/django-project.git`.

2. Install and activate virtual environment in the same directory using pip

#Check if pip is installed on your system.
`python3 -m pip --version`.

#Upgrade pip version if needed.
`python3 -m pip install --user --upgrade pip`.

#Install Virtual environment and activate it.
`python3 -m venv env`.

`source env/bin/activate`.

3. Change directory into ***django-project***.

`cd django-project`.

4. Install all the dependecies needed to run the application.

`pip install -r requirements.txt`.

5. Change your own keys that are inside the env file

6. Migrate database models.

 `python manage.py makemigarations`.
 `python manage.py migrate`.
 
 7. Run the application and open in browser.
 
 `python manage.py runserver`.
 
 
