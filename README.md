# Users exercise <!-- omit in toc -->

- [About the project](#about-the-project)
  - [Exercise](#exercise)
  - [Built with](#built-with)
- [Getting started](#getting-started)
  - [Installation](#installation)
  - [Project structure](#project-structure)
- [API](#api)
- [Usage](#usage)
- [How to](#how-to)
  - [How to receive Kafka notifications](#how-to-receive-kafka-notifications)
- [Roadmap](#roadmap)
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
* ipapi
* kafka

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

### Project structure
>NB: if you are not familiar with Django projects, you may want to check the [documentation](https://docs.djangoproject.com/en/3.1/). This short [tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/) covers the creation of a project and the directory structure for instance.

In this project:
- the `users_service` directory is the Python package for the project. In particular, it contains the settings of the project and the URL declarations. 
- the `users` directory is the Python package for the application to handle users.

## API

Endpoint | Method | Result
--- | --- | ---
/api/v1/users | GET | Get all users.
/api/v1/users/:id | GET | Get user by id.
/api/v1/users | POST | Create a new user.
/api/v1/users/:id | PATCH | Partial update a user by id.
/api/v1/users/:id | PUT | Update a user by id.
/api/v1/users/:id | DELETE | Delete user by id.

Upon data change (POST, PUT, PATCH, DELETE), a notification event is sent on a Kafka topic if the Kafka environment is up and running:
```json
{
   'action': 'post', 
   'data': {
      "id": 1, 
      "first_name": "Serge", 
      "last_name": "Karamazov", 
      "email": "skara@mail.com", 
      "password": "myP@ssW0ord52", 
      "address": "5 rue de la poste Paris"
      }
}
```


## Usage

To start the service, run the following command:
```bash
users-exercise/users_django$ python manage.py runserver
```
You can use the Django REST Framework browsable API to access the API: http://localhost:8000/api/v1/users

or using [httpie](https://github.com/httpie/httpie#installation) command line tool:
```json
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
```json
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

### How to receive Kafka notifications

Download Kafka and follow the [quickstart guide](https://kafka.apache.org/quickstart) to start Kafka environment and create your topic. Make sure to register the topic name in the `users_django/users/kafka/conf.yml` file.

with python :

make sure to activate your virtualenv or run:
```bash
pip install kafka-python
```

```python
>>> from kafka import KafkaConsumer
>>> import json
>>> consumer = KafkaConsumer(bootstrap_servers='localhost:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
>>> consumer.subscribe('users-events')
>>> for msg in consumer:
...     print(msg.value)
{'action': 'delete', 'data': {"url": "http://testserver/api/v1/users/1", "id": 1, "first_name": "Serge", "last_name": "Karamazov", "email": "skara@mail.com", "password": "myP@ssW0ord52", "address": "5 rue de la poste Paris"}}
```
it returns consuùerrecord cf github link


or using Kafka consumer console as described in the [quickstart guide](https://kafka.apache.org/quickstart):
```bash
$ bin/kafka-console-consumer.sh --topic users-events --from-beginning --bootstrap-server localhost:9092
```

## Roadmap
This API has been implemented in a very short timeframe and there are few limitations to consider (non exhaustive list):
- [ ] Authentication and authorization were out of scope, but Django REST framework supports [authentication]  (https://www.django-rest-framework.org/api-guide/authentication/) and [permissions](https://www.django-rest-framework.org/api-guide/permissions/).
- [ ] Passwords are stored and returned in plain text. Instead, we could for instance extend the Django `User` model to [manage passwords](https://docs.djangoproject.com/en/3.1/topics/auth/passwords/) or obfuscate passwords using a [custom field](https://www.django-rest-framework.org/api-guide/fields/#custom-fields) trick.
- [ ] Logging is currently limited to the print of messages to the standard output for the sake of the exercise. I'd recommend to use Python logging facility for proper logging with the relevant level of information(DEBUG, INFO, WARNING, ERROR). Logging a unique transaction ID for each request could also ease the investigation.
- [ ] Deployment through Docker for instance.
- [ ] Kafka producer can be improved, for instance: 
  - configuration can be extended. 
  - New events could be published in case of failure to notify the other services.
  - Mock for the tests.
- [ ] 

## License
Distributed under the MIT License. See LICENSE for more information.

## Contact
Project link: https://github.com/r-o-main/users-exercise
