# Deploy Development Environment:
The development environment is created to run in a Desktop for a developer, using sqlite as database (a file), with a python virtual-environment (to install requirements) and to run django app. If needed, Stripe integrations are set using the Stripe CLI, also installed in the Desktop.

The most recent code for Dev Environment is found inside the dev branch. To get it, make sure you have access to platoe repository, and in a working directory, run the commands and populate with your credentials.

```
git clone -b dev https://github.com/videap/platoe
```

# Project Structure:

### Django Structure
This project is called plato, and has 1 configured application inside, called ideas. Some configurations are set in the project level, other in the application level.

### Python Packages
They are all defined in the file **requirements.txt**

### Stripe API Keys
The communication with stripe uses API keys for authentication and they must be defined as ENVIRONMENT VARIABLES. You can get the keys with the Admin for the Stripe Account. Below are the variables that must be set:

 - STRIPE_PUBLISHABLE_KEY
 - STRIPE_SECRET_KEY
 - WEBHOOK_SECRET

### Stripe Credit Card for Test
To test payment options, you can use the test card for Stripe, defined by:
  4242 4242 4242 4242

### manage.py
This file is in the root project directory, and is the main file to control django.

### urls.py
The urls file describes all paths for the application. Each path calls for a function inside the views.py, and passes the web request alongside with the defined parameters.
There are 2 urls.py files, the project file, and the application file. The project file is global and is currently configured to include all paths defined in the application urls.py file.


## Components
All components are inside the *idea* folder.

### media/ and media/profile_images/
These folders are to maintain images and media files. They are served by django in developer environment and configured in the dev-settings.py file. They expose the files found in the MEDIA_ROOT directory using the MEDIA_URL string. For example, a request for plato.io/media/profile_images/user1.png would fetch for an image named user1.png found in the MEDIA_ROOT/profile_mages/ directory.

### static/
This folder holds the CSS and Javascript files, and is also served by django in developer environment. Similar to media, they expose the files found in the STATIC_ROOT directory using the STATIC_URL string

### templates/*.html files

All .html files render the HTML and some javascript code, for each page.

### /static/ideas/react_components.js
All react elements (classes) are defined here, and only that.

### api.py
Defines all functions called by the server or the front-end, mostly to manage data.

### api_stripe.py
Defines functions to interact with stripe. All functions are called by the server side, with information fetched from the database.

### forms.py
Most of the data inserted with POST requests are validated by Django using ModelForms. This file defines the classes used.  

### functions.py
General functions used by views and APIs, such as Paginator and custom validation.

# HOW TO DEPLOY

## 1. Get the code

The most recent code for Dev Environment is found inside the dev branch. To get it, make sure you have access to platoe repository, and in a working directory, run the commands and populate with your credentials.

```
git clone -b dev https://github.com/videap/platoe
```

## 2. Create a virtual environment (for python)
Assuming you are working with a windows desktop, you need first to install Python3.8 and the virtualenv package for windows.

[Download and run the executable for Python3.8](https://www.python.org/ftp/python/3.8.0/python-3.8.0.exe) and configure path variables accordingly. Check your installation running in a terminal the commands:
```
python -V
pip -V
```
The expected output is the version 3.8 of Python and pip (packager installer).
To install the virtualenv package, run:
```
pip install virtualenv
```

To create your virtualenv environment in a folder called "venv" you can run the following command from the directory you want to work. You will access this directory to activate or deactivate the virtual environment:

```
virtualenv venv
```

To activate the virtualenv, run the activate script inside the venv folder. For example, in a terminal, use the command:
```
venv/Scripts/activate

```

## 3. Install Plato required modules
Make sure you are working in the project root directory. This directory is where you find the manage.py file.

Plato uses from several external modules that need to be installed using pip. The virtualenv has its own pip installation, so you can install all modules using the requirements.txt file, running:
```
pip install -r ./requirements.txt
```
## 5. Populate the database with dev data using the fixtures
To populate de sqlite database using the fixtures, run the command:
```
python manage.py loaddata ./fixtures/db.json
```

## 6. Run django using testserver functionality
Django has a test server embedded for development purposes, that always runs locally. To run:
```
python manage.py runserver
```

To check if the application is running properly, from the same machine that is running the server, access from any browser:
>http://localhost:8000

## 7. Install and Run Stripe Webhook Locally
Finally, if you need to develop using the stripe webhook for payment capabilities, you need to set up a local webhook, simulating an exposed webhook for production.
[Check stripe documentation](https://stripe.com/docs/webhooks/test). It will show you how to install the Stripe CLI in the dev environment. 

To simulate the webhook, run the following command in a terminal:

    stripe listen --forward-to localhost:8000/stripe_webhook
   
  > **Note:** If needed, change "localhost:8000" accordingly, this must be a resolvable address:port to Django Server

When you run the "stripe listen" command, it will show you the WEBHOOK secret needed for this configurations. The keys can be shared with you by the stripe account admin. When you have all the information needed, set up the environment variables and restart django server.
 
 - STRIPE_PUBLISHABLE_KEY="pk_test_....................."
 - STRIPE_SECRET_KEY="sk_test_....................." 
 - WEBHOOK_SECRET="whsec_..............."


