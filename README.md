[![Build Status](https://travis-ci.org/ruganda/Ride-api.svg?branch=develop)](https://travis-ci.org/ruganda/Ride-api)
[![Coverage Status](https://coveralls.io/repos/github/ruganda/Ride-api/badge.svg?branch=develop)](https://coveralls.io/github/ruganda/Ride-api?branch=develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/36b826ffbeae475d95b7d6be8773a178)](https://www.codacy.com/app/ruganda/Ride-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ruganda/Ride-api&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/78ffc2eb1c22277b0725/maintainability)](https://codeclimate.com/github/ruganda/Ride-api/maintainability)

# Ride-api
Ride-my App is a carpooling application that provides drivers with the ability to create ride offers and passengers  to join available ride offers.

**Application Features**

* Creating Rides
* Send request to join an existing ride
* Accept/ reject a ride request 


# A user can perform the following :
 As a passenger:
- Can view all ride offers
- Can create a ride offer
- Can view a specific ride offer
- Make a request to join a ride.
 
 As a driver:
- Create a ride offer
- Can accept/reject ride request

**Application demo**
* The documentation can be accessed at https://rideapi1.docs.apiary.io/#
    - To interact with the documentation, https://private-amnesiac-b7e82-rideapi1.apiary-proxy.com/api/v2/rides/
* To interact with the application via postman
     * https://rugandaride.herokuapp.com/api/v2/rides/

    then use the following endpoints to perform the specified tasks
    
    EndPoint                                           | Functionality
    ------------------------                           | ----------------------
    POST /auth/register                                | Create a user account
    POST /auth/login                                   | Log in a user
    POST /users/rides/                                 | Create a new ride
    GET /rides/                                        | Retrieves all rides
    GET /users/rides/                                  | Retrieves all rides that are created by the user
    POST /rides/< ride_id >/requests                   | Send passenger's request to join a ride
    GET  /users/rides/< ride_id >/requests             | Retrieve passengers who requested to join the ride
    PUT /users/rides/< irde_id >/requests/< r_id>      | Update a ride request

    
**Getting started with the app**

**Technologies used to build the application**

* [Python 3.6](https://docs.python.org/3/)

* [Flask](http://flask.pocoo.org/)

* [PostgreSQL](https://www.postgresql.org/)

* [JWT](auth0.com/docs/jwt)

# Installation

Create a new directory and initialize git in it. Clone this repository by running
```sh
$ git clone https://github.com/ruganda/Ride-api.git
```
Create a virtual environment. For example, with virtualenv, create a virtual environment named venv using
```sh
$ virtualenv venv
```
Activate the virtual environment
```sh
$ cd venv/scripts/activate.bat
```
Install the dependencies in the requirements.txt file using pip
```sh
$ pip install -r requirements.txt
```

Start the application by running
```sh
$ python run.py
```
Test your setup using a client app like postman

**Running tests**

* Install nosetests 
* navigate to project root
* Use `nosetests tests/` to run the tests
* To run tests with coverage, use `nosetests --with-coverage --cover-package=app && coverage report`