# SoftDesk

SoftDesk is a Django RESTful API for managing to-do lists within IT Teams.

# Description

* Access is granted to authenticated users via JSON Web Tokens (JWTs);

* To-do lists include projects;
* Each project can include issues;
* Each issue can include comments;

* Only project contributors can access the details of a project (contributors, issues, comments).
* Only the author of a project/issue/comment can update or delete it.


# Run SoftDesk

## Clone application

* Clone SoftDesk application in your target folder: `git clone https://github.com/Alexandremerancienne/SoftDesk`

## Install packages

* Create a virtual environment (venv).

* Activate your venv, then install packages listed in requirements.txt file : `pip install -r requirements.txt`

## Launch server

* Launch local server from your terminal: `python manage.py runserver`

## Test endpoints

* Endpoints can be tested with tools such as Postman or cURL.

* A Public Postman collection is available to test the API endpoints : `https://documenter.getpostman.com/view/15000046/Tzeaj6GQ`
