[![Build Status](https://travis-ci.com/wakandavibranium/Store-Manager-API-V2.svg?branch=bg-fix-travis-yml-%23161576046)](https://travis-ci.com/wakandavibranium/Store-Manager-API-V2)  [![Coverage Status](https://coveralls.io/repos/github/wakandavibranium/Store-Manager-API-V2/badge.svg?branch=ch-integrate-heroku-%23161433650)](https://coveralls.io/github/wakandavibranium/Store-Manager-API-V2?branch=ch-integrate-heroku-%23161433650)  [![Maintainability](https://api.codeclimate.com/v1/badges/bea1b838773f4effe438/maintainability)](https://codeclimate.com/github/wakandavibranium/Store-Manager-API-V2/maintainability)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/4394c410e549319bac77)

# Store-Manager-API-V2
This is an API for the Store Manager web application. Store Manager is a web application that helps store owners manage sales and product inventory records.


## Documentation

1. API documentation can be found [here](https://store-manager-api-adc3.herokuapp.com/api/v2)

2. PivotalTracker stories can be found [here](https://www.pivotaltracker.com/n/projects/2202783)


## Prerequisites

1. Download & install [Python 3+](https://www.python.org/downloads/)

2. Download & install [Git](https://git-scm.com/downloads) 

3. Download & install [Postman](https://www.getpostman.com/apps)


## Installation & Configurations

1. Create a directory and `cd` into it

2. ```git clone https://github.com/wakandavibranium/Store-Manager-API-V2.git```

3. `cd` into the Store-Manager-API-V2 repo

4. ```git checkout develop```

5. Create a [virtual environment](https://virtualenv.pypa.io/en/stable/) for this project and activate it.

6. Open the terminal and type ```pip install -r requirements.txt``` 
   This will install project dependancies.

### Configuring environment variables on windows, 
```
set FLASK_APP=run.py
set FLASK_ENV=development
set SECRET_KEY=thisisyoursecretkey
set DATABASE_URL=postgresql://myusername:mypassword@localhost:5432/my_database
```

### Configuring environment variables on linux, 
```
export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY=thisisyoursecretkey
export DATABASE_URL=postgresql://myusername:mypassword@localhost:5432/my_database
```

## Running The App
On your terminal

```flask run```

## Consuming the API

* Open your web browser and enter ```http://127.0.0.1:5000/api/v2``` in the address bar

```or```

* Visit the API hosted on [Heroku](https://store-manager-api-adc3.herokuapp.com/api/v2)


## API Endpoints Implemented

| HTTP Method   |  EndPoint             | Description                             |
| --------------|:----------------------|:---------------------------------------:|                                                                 
| POST          | /products/            | Add a product                           | 
| GET           | /products/            | Get all products                        | 
| GET           | /products/{id}        | Get a product by id                     |
| PUT           | /products/{id}        | Edit a product by id                    |
| DELETE        | /products/{id}        | Delete a product by id                  |
| POST          | /sales/               | Add a sale                              |
| GET           | /sales/               | Get all sales                           |
| GET           | /sales/{id}           | Get a sale by id                        |
| POST          | /auth/signup/         | Sign Up a user                          |
| POST          | /auth/login/          | Login a user                            |
