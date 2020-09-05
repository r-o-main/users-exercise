# Users exercise <!-- omit in toc -->

- [About the project](#about-the-project)
  - [Exercise](#exercise)
  - [Built with](#built-with)
- [Getting started](#getting-started)
  - [Installation](#installation)
- [Usage](#usage)
- [API](#api)
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

## Usage

## API

## How to

## Issues

## License
Distributed under the MIT License. See LICENSE for more information.

## Contact
Project link: https://github.com/r-o-main/users-exercise
