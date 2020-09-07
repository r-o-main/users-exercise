# Users exercise <!-- omit in toc -->

- [About the project](#about-the-project)
  - [Exercise](#exercise)
  - [Built with](#built-with)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Project structure](#project-structure)
- [Users API](#users-api)
  - [Resource URL](#resource-url)
  - [Resource information](#resource-information)
  - [Endpoints](#endpoints)
  - [Query parameters](#query-parameters)
  - [User model](#user-model)
  - [Examples](#examples)
  - [Get all users](#get-all-users)
      - [Request](#request)
      - [Response 200](#response-200)
  - [Create a user](#create-a-user)
    - [Create a valid user](#create-a-valid-user)
      - [Request](#request-1)
      - [Response 201](#response-201)
    - [Create an invalid user](#create-an-invalid-user)
      - [Request](#request-2)
      - [Response 400](#response-400)
    - [Create a user with an IP address not from Switzerland](#create-a-user-with-an-ip-address-not-from-switzerland)
      - [Request](#request-3)
      - [Response 403](#response-403)
  - [Get single user](#get-single-user)
    - [Valid user](#valid-user)
      - [Request](#request-4)
      - [Response 200](#response-200-1)
    - [Invalid user](#invalid-user)
      - [Request](#request-5)
      - [Response 404](#response-404)
- [Update single user](#update-single-user)
    - [Valid user](#valid-user-1)
      - [Request](#request-6)
      - [Response 200](#response-200-2)
    - [Invalid user](#invalid-user-1)
      - [Request](#request-7)
      - [Response 404](#response-404-1)
- [Delete single user](#delete-single-user)
    - [Valid user](#valid-user-2)
      - [Request](#request-8)
      - [Response 204](#response-204)
    - [Invalid user](#invalid-user-2)
      - [Request](#request-9)
      - [Response 404](#response-404-2)
- [Notifications](#notifications)
- [Usage](#usage)
  - [Start the service](#start-the-service)
  - [Use the API](#use-the-api)
- [How to](#how-to)
  - [How to launch the tests](#how-to-launch-the-tests)
  - [How to receive the Kafka notifications](#how-to-receive-the-kafka-notifications)
    - [Setup](#setup)
    - [From the Kafka consumer console](#from-the-kafka-consumer-console)
    - [From the python interpreter](#from-the-python-interpreter)
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

- **Python 3.8.2**
- [Django](https://www.djangoproject.com)
- [Django REST framework](https://www.django-rest-framework.org)
- [ipapi](https://github.com/ipapi-co/ipapi-python)
- [kafka-python](https://github.com/dpkp/kafka-python)

## Getting started

### Prerequisites

>The examples of commands below are applicable for Linux. For other OS, please refer to the [documentation](https://virtualenv.pypa.io/en/stable/).

Before starting, it is recommended to ensure pip, setuptools and wheel are up to date:
```bash
pip install -U pip setuptools wheel
```

### Installation
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
   ~/projects/ricardo-project/users-exercise/users_django$ python manage.py migrate
   ```

### Project structure
>NB: if you are not familiar with Django projects, you may want to check the [documentation](https://docs.djangoproject.com/en/3.1/). This short [tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/) covers the creation of a project and the directory structure for instance.

In this project:
- the `users_service` directory is the Python package for the project. In particular, it contains the settings of the project and the URL declarations. 
- the `users` directory is the Python package for the application to handle users.

## Users API

### Resource URL

`http://127.0.0.1:8000/api/v1/users`[.json]

### Resource information

- Response formats: JSON
- Requires authentication: No

### Endpoints

Endpoint | Method | Result | Parameters 
 --- | --- | --- | --- 
/api/v1/users | GET | Get all users | None
/api/v1/users | POST | Create a new user if IP address is located in Switzerland | None
/api/v1/users/:id | GET | Get user by id | User id `REQUIRED`
/api/v1/users/:id | PATCH | Partial update a user by id | User id `REQUIRED`
/api/v1/users/:id | PUT | Update a user by id | User id `REQUIRED`
/api/v1/users/:id | DELETE | Delete user by id | User id `REQUIRED`

### Query parameters

Parameter | Required | Usage | Description | Example
--- | --- | --- | --- | --- 
`last_name` | optional | Filter | Filter on user last name field (case sensitive). | `/api/v1/users/?last_name=Deray`
`first_name` | optional | Filter | Filter on user first name field (case sensitive). | `/api/v1/users/?last_name=Deray&first_name=Odile`
`search` | optional | Search | Search in the user last name and email fields (case sensitive).| `api/v1/users?search=oderay`
`page` | optional | Pagination | Set the current page. | `api/v1/users/?page=2   `
`page_size` | optional | Pagination | The maximun number of users to return per page. | `api/v1/users/?page=2&page_size=4`

### User model

To create a user, the following fields must be filled:
```json
{
   "first_name": "Serge",
   "last_name": "Karamazov",
   "email": "s.kara@mail.com",
   "password": "myP@ssW0ord52",
   "address": ""
}
```
>Please note that:
> - The `password` field is returned in plain text in this version. The [Roadmap](#roadmap) section contains information on how to secure it.
>- The `address` field can be empty.
>- An `id` is automatically created for each user.
>- The `email` field should be unique (only one user with the same email).

### Examples

### Get all users
Returns a collection of users.

##### Request
```
GET /api/v1/users
```
##### Response 200
```json
TTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://127.0.0.1:8000/api/v1/users/1",
            "id": 1,
            "first_name": "Serge",
            "last_name": "Karamazov",
            "email": "s.kara@mail.com",
            "password": "myP@ssW0ord52",
            "address": "Paris"
        },
        {
            "url": "http://127.0.0.1:8000/api/v1/users/2",
            "id": 2,
            "first_name": "Odile",
            "last_name": "Deray",
            "email": "oderay@mail.com",
            "password": "myP@ssw0rd49",
            "address": ""
        },
        {
            "url": "http://127.0.0.1:8000/api/v1/users/3",
            "id": 3,
            "first_name": "John",
            "last_name": "Malkovitch",
            "email": "john_m@mail.com",
            "password": "pzd369",
            "address": "Russia"
        }
    ]
}
```

### Create a user
Returns the newly created user with its `id` and `url`.

#### Create a valid user
IP address should be located in Switzerland and `first_name`, `last_name`, `email`, `password` fields are filled.

##### Request
```
POST /api/v1/users
```

Body:
```json
{
   "first_name": "Serge",
   "last_name": "Karamazov",
   "email": "s.kara@mail.com",
   "password": "myP@ssW0ord52",
   "address": ""
}
```

##### Response 201
```json
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Location: http://127.0.0.1:8000/api/v1/users/53
Vary: Accept

{
    "url": "http://127.0.0.1:8000/api/v1/users/53",
    "id": 53,
    "first_name": "Serge",
    "last_name": "Karamazov",
    "email": "s.kara@mail.com",
    "password": "myP@ssW0ord52",
    "address": ""
}

```

#### Create an invalid user
Either `first_name`, `last_name`, `email` or `password` fields are not filled.

##### Request
```
POST /api/v1/users
```

Body:
```json
{
   "first_name": "Serge",
   "last_name": "Karamazov",
   "email": "s.kara@mail.com",
   "address": ""
}
```

##### Response 400
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "email": [
        "user with this email already exists."
    ],
    "password": [
        "This field is required."
    ]
}
```

#### Create a user with an IP address not from Switzerland

##### Request
```
POST /api/v1/users
```

Body:
```json
{
   "first_name": "Serge",
   "last_name": "Karamazov",
   "email": "s.kara@mail.com",
   "password": "myP@ssW0ord52",
   "address": ""
}
```

##### Response 403
```json
HTTP 403 Forbidden
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Only users located in Switzerland can be created (remote address in France)"
}
```

### Get single user
Returns the user matching the provided user id.

#### Valid user

##### Request
```
GET /api/v1/users/1
```

##### Response 200
```json
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "url": "http://127.0.0.1:8000/api/v1/users/1",
    "id": 1,
    "first_name": "Serge",
    "last_name": "Karamazov",
    "email": "s.kara@mail.com",
    "password": "myP@ssW0ord52",
    "address": "Paris"
}
```

#### Invalid user

##### Request
```
GET /api/v1/users/100
```

##### Response 404
```json
HTTP 404 Not Found
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Not found."
}
```

## Update single user
Returns the modified user matching the provided user id.

#### Valid user

##### Request
```
PATCH /api/v1/users/1
```
Body:
```json
{
    "address": "NYC"
}
```

##### Response 200
```json
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "url": "http://127.0.0.1:8000/api/v1/users/1",
    "id": 1,
    "first_name": "Serge",
    "last_name": "Karamazov",
    "email": "s.kara@mail.com",
    "password": "myP@ssW0ord52",
    "address": "NYC"
}
```

#### Invalid user

##### Request
```
PATCH /api/v1/users/100
```
Body:
```json
{
    "address": "NYC"
}
```

##### Response 404
```json
HTTP 404 Not Found
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Not found."
}
```

## Delete single user
Delete the user matching the provided user id.

#### Valid user

##### Request
```
DELETE /api/v1/users/1
```

##### Response 204
```json
HTTP 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```

#### Invalid user

##### Request
```
DELETE /api/v1/users/100
```

##### Response 404
```json
HTTP 404 Not Found
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Not found."
}
```

## Notifications
Upon data change (`POST`, `PUT`, `PATCH`, `DELETE`), a notification event is sent on a Kafka topic if the Kafka environment is up and running:
```json
{
   "action": "create", 
   "data": {
      "id": 1, 
      "first_name": "Serge", 
      "last_name": "Karamazov", 
      "email": "s.kara@mail.com", 
      "password": "myP@ssW0ord52", 
      "address": "Paris"
      }
}
```

## Usage

### Start the service
Run the following command:
```bash
users-exercise/users_django$ python manage.py runserver
```

### Use the API
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
    "id": 4,
    "last_name": "Doe",
    "password": "pwd0@39"
}
```

or using `curl`:
```json
$ curl -X GET -H 'Accept: application/json; indent=4' -i  http://127.0.0.1:8000/api/v1/users/2
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
    "id": 2,
    "first_name": "Odile",
    "last_name": "Deray",
    "email": "oderay@mail.com",
    "password": "myP@ssw0rd49",
    "address": ""
}
```

## How to

### How to launch the tests
```bash
users-exercise/users_django$ python manage.py test
```

### How to receive the Kafka notifications

#### Setup
Download Kafka and follow the [quickstart guide](https://kafka.apache.org/quickstart) to start Kafka environment and create your topic (here `users-events`). Make sure to register the topic name in the `users_django/users/kafka/conf.yml` file.

You are now ready to receive notifications.

#### From the Kafka consumer console
As described in the [quickstart guide](https://kafka.apache.org/quickstart):
```bash
$ bin/kafka-console-consumer.sh --topic users-events --from-beginning --bootstrap-server localhost:9092
```

#### From the python interpreter
Make sure to first activate your virtualenv or run:
```bash
$ pip install kafka-python
```

Then start the [python interpreter](https://docs.python.org/3/tutorial/interpreter.html):
```bash
$ python
```

And create a simple Kafka consumer that subscribes on the topic you created (here `users-events`):
```python
>>> from kafka import KafkaConsumer
>>> import json
>>> consumer = KafkaConsumer(bootstrap_servers='localhost:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
>>> consumer.subscribe('users-events')
>>> for msg in consumer:
...     print(msg.value)
```

>Messages received are of type `ConsumerRecord`:
>```python
>ConsumerRecord = collections.namedtuple("ConsumerRecord",
>    ["topic", "partition", "offset", "timestamp", "timestamp_type",
>     "key", "value", "headers", "checksum", "serialized_key_size", "serialized_value_size", "serialized_header_size"])
>```
>Source: https://github.com/dpkp/kafka-python/blob/master/kafka/consumer/fetcher.py

Example of notification:
```json
{"action": "delete", "data": {"url": "http://testserver/api/v1/users/1", "id": 1, "first_name": "Serge", "last_name": "Karamazov", "email": "s.kara@mail.com", "password": "myP@ssW0ord52", "address": "Paris"}}
```

## Roadmap
This API has been implemented in a very short timeframe and there are few limitations to consider (non exhaustive list):
- [ ] Authentication and authorization were out of scope, but Django REST framework supports [authentication]  (https://www.django-rest-framework.org/api-guide/authentication/) and [permissions](https://www.django-rest-framework.org/api-guide/permissions/).
- [ ] Obviously passwords: they are stored and returned in plain text. Instead, we could for instance extend the Django `User` model to [manage passwords](https://docs.djangoproject.com/en/3.1/topics/auth/passwords/) or obfuscate passwords using a [custom field](https://www.django-rest-framework.org/api-guide/fields/#custom-fields) trick. My personal preference would go for an access token system as much as possible.
- [ ] Logging is currently limited to the print of messages to the standard output for the sake of the exercise. I'd recommend to use Python logging facility for proper logging with the relevant level of information(DEBUG, INFO, WARNING, ERROR). Logging a global unique ID per transaction could also ease the traceability and troubleshooting (especially in a distributed environment).
- [ ] Current Kafka producer is very simple and can be extended, for instance: 
  - Using the parameters defined in https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
  - For each action modifying users data, the data is pushed to kafka upon success only. But if the push to kafka fails, it may end up with data modified in database and no events sent to notify other services of the modification. The retry mechanism of Kafka can help, but for non-retriable exceptions, if these notifications modify the state of other services, the SAGA pattern microservice architecture could help mitigating dual writes issues. New events could be published in case of failure to notify the other services or rollback the change.
  - Mock for the tests.
  - When kafka environment is not set or down, there is an impact on the performance of the API.
- [ ] Sqlite database is suitable for this exercise, but for better security and scalability, other RDMS like MySQL or PostgreSQL are probably more suitable.
- [ ] The server is not setup for production. Containerizing the application with Docker would be a good option on top of that to create a production-ready setup.
- [ ] Adding a detailed reference documentation for the API.
- [ ] Users API could have more parameters, for instance:
    - `country` to return users with address located in a country
    - `since_id` to return users with id greater than since_id
    - `max_id` to return users with id less than max_id
    - `until` to return users created before a date (requires to add creation date)
    - etc.

## License
Distributed under the MIT License. See LICENSE for more information.

## Contact
Project link: https://github.com/r-o-main/users-exercise
