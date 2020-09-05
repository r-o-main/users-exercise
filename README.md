# Users exercise <!-- omit in toc -->

- [About the project](#about-the-project)
  - [Exercise](#exercise)
  - [Built with](#built-with)
- [Getting started](#getting-started)
  - [Installation](#installation)
- [API](#api)
- [Usage](#usage)
- [How to](#how-to)
- [Issues](#issues)
- [License](#license)
- [Contact](#contact)

## About the project
Homework exercise for a technical interview @ricardo.ch.

### Exercise
>A user is defined by the following attributes: email, password, first name and an address.
>
>Build a REST API micro-service to handle users. It should provide basic operations such as creating a user, updating full and partial user data, and retrieving one or many users based on various filter (eg.: first name, email).
>
>On a user creation request, you should check if the user is located in Switzerland. Only if he is, you should allow the user creation, otherwise the request must be rejected. You can use the user IP address and https://ipapi.co/ to geolocate it.
>
>On each mutating operation, a JSON formatted event must be produced to a service bus (Kafka, RabbitMQ...). Those events would be, in a real world scenario, used to notify other micro-services of a data change and conduct some business logic (sending emails, analytics...).
>
>As a database, we ask you to use any relational option you see fit.
>
>Authentication and authorisation are out of scope.

### Built with

* Python 3.8.2
* [Django](https://www.djangoproject.com)
* [Django REST framework](https://www.django-rest-framework.org)

## Getting started

### Installation

>The examples of commands below are applicable for Linux. For other OS, please refer to the [documentation](https://virtualenv.pypa.io/en/stable/).

1. Create a virtualenv and activate it, for instance:
   ```bash
    ~/projects$ mkdir ricardo-project && cd ricardo-project
    ~/projects/ricardo-project$ python -m virtualenv env
    ~/projects/ricardo-project$ . env/bin/activate
   ```
2. Clone the repository:
   ```bash
   ~/projects/ricardo-project$ git clone https://github.com/r-o-main/users-exercise.git
   ```
3. Install the requirements:
   ```bash
   ~/projects/ricardo-project$ cd users-exercise
   ~/projects/ricardo-project/users-exercise$ pip install -r requirements.txt
   ```
4. Generate the sqlite database to store the users:
   ```bash
   ~/projects/ricardo-project/users-exercise$ python manage.py migrate
   ```

## API

Endpoint | Method | Result
--- | --- | ---
/api/v1/users | GET | Get all users.
/api/v1/users/:id | GET | Get user by id.
/api/v1/users | POST | Create a new user.
/api/v1/users/:id | PATCH | Partial update a user by id.
/api/v1/users/:id | PUT | Update a user by id.
/api/v1/users/:id | DELETE | delete user by id.

## Usage

To start the service, run the following command:
```bash
~/projects/ricardo-project/users-exercise$ python manage.py runserver
```
You can use the Django REST Framework browsable API to access the API: http://localhost:8000/api/v1/users

or using [httpie](https://github.com/httpie/httpie#installation) command line tool:
```bash
$ http POST http://127.0.0.1:8000/api/v1/users last_name=Doe first_name=John email=john@example.org password=pwd0@39
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 107
Content-Type: application/json
Date: Sat, 05 Sep 2020 17:49:32 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.2
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "address": "",
    "email": "john@example.org",
    "first_name": "John",
    "id": 1,
    "last_name": "Doe",
    "password": "pwd0@39"
}
```

or using `curl`:
```bash
$ curl -X GET -H 'Accept: application/json; indent=4' -i  http://127.0.0.1:8000/api/v1/users/1
HTTP/1.1 200 OK
Date: Sat, 05 Sep 2020 17:52:03 GMT
Server: WSGIServer/0.2 CPython/3.8.2
Content-Type: application/json
Vary: Accept, Cookie
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 151
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

{
    "id": 1,
    "first_name": "Odile",
    "last_name": "Deray",
    "email": "oderay@mail.com",
    "password": "myP@ssw0rd49",
    "address": ""
}
```

## How to

## Issues

## License
Distributed under the MIT License. See LICENSE for more information.

## Contact
Project link: https://github.com/r-o-main/users-exercise
