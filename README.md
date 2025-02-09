<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [] instead of parentheses ().
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- HIDDEN TAG FOR BACK TO TOP LINKS -->
<a id="readme-top"></a>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#setup">Setup</a>
      <ul>
        <li><a href="#clone-the-repository">Clone the Repository</a></li>
        <li><a href="#install-requirements">Install Requirements</a></li>
        <li><a href="#create-env-variables">Create .env Variables</a></li>
        <li><a href="#setup-postgresql-database">Setup PostgreSQL Database</a></li>
        <li><a href="#run-the-app">Run the App</a></li>
      </ul>
    </li>
    <li><a href="#rest-api---endpoints">Endpoints</a></li>
      <ul>
        <li><a href="#create-a-new-user">Create a New User</a></li>
        <li><a href="#login-fetch-token">Login (fetch token)</a></li>
        <li><a href="#get-a-list-of-characters">Get a List of Characters</a></li>
        <ul>
            <li><a href="#pagination">Pagination</a></li>
            <li><a href="#filtering">Filtering</a></li>
            <li><a href="#sorting">Sorting</a></li>
        </ul>
        <li><a href="#get-character-by-id">Get Character by ID</a></li>
        <li><a href="#create-a-new-character">Create a New Character</a></li>
        <li><a href="#update-a-character">Update a Character</a></li>
        <li><a href="#delete-a-character">Delete a Character</a></li>
      </ul>
    <li><a href="#data-models">Data Models</a></li>
      <ul>
        <li><a href="#user">User</a></li>
        <li><a href="#character">Character</a></li>
      </ul>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# REST API

### About the project

This is a REST API built as a software engineering assignment for webeet.io </br>
Provided was a list of Game of Thrones characters, which the user can query.
Basic CRUD operations are implemented, as well as pagination, filtering and sorting — separately or simultaneously.
This API uses a PostgreSQL database, includes user authentication and authorization
and features some basic unit testing.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Flask][Flask]][Flask-url]
* [![JWT][JWT]][JWT-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Setup

## Clone the repository

using GitHub CLI:

    gh repo clone Tombunzel/webeetGotAssignment

using git:

    git clone https://github.com/Tombunzel/webeetGotAssignment.git

[Troubleshooting cloning](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#troubleshooting-cloning-errors)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Install requirements

Make sure you are in the main folder of the project, then run:

    pip install -r requirements.txt

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Create .env variables

The API requires a .env file with the following variables:
  - `JWT_KEY`: secret key for secure token creation and verification (HS256) 
  - `SQLALCHEMY_DATABASE_URL`: connection string with necessary details for database connection. (`postgresql+psycopg2://username:password@host:port/database-name`)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Setup PostgreSQL database

    python3 setup_database.py

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Import characters from the provided JSON file to the database

    python3 insert_characters_from_json_to_database.py

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Run the app

    python3 app.py


<p align="right">(<a href="#readme-top">back to top</a>)</p>


# REST API - Endpoints

Listed below are the API's endpoints


## Create a new user

Use this endpoint to create a user.

### Request

URL: `.../signup`

METHOD: `POST`

BODY:

    {
        "username": "your-username",
        "password": "your-password"
    }

### Response

    HTTP/1.1 201 Created
    Status: 201 Created
    Server: Werkzeug/2.3.7 Python/3.12.2
    Date: Sat, 08 Feb 2025 16:23:38 GMT
    Content-Type: application/json
    Content-Length: 32
    Connection: close

    {"message": "User created"}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Login (fetch token)

Use this endpoint to log in to an existing user and receive a token.

This token allows you to make requests to endpoints which require authorization.
The token is valid for 30 minutes.
After that, a new token must be generated by making a request to the `.../login` endpoint

### Request

URL: `.../login`

METHOD: `POST`

BODY:

    {
        "username": "your-username",
        "password": "your-password"
    }

### Response

    HTTP/1.1 201 Created
    Status: 201 Created
    Server: Werkzeug/2.3.7 Python/3.12.2
    Date: Sat, 08 Feb 2025 16:23:38 GMT
    Content-Type: application/json
    Content-Length: 133
    Connection: close

    {"token": "your-authorization-token"}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Get a list of characters

URL: `.../api/characters`

METHOD: `GET`

### Pagination

Pagination is handled through the query arguments `skip` and `limit`, e.g.:

    `.../api/characters?skip=20&limit=10`

This will result in 20 characters being skipped, and the next 10 being included in the results.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Filtering

The user can choose to filter through the characters by each attribute available:
`age`, `name`, `house`, `animal`, `death`, `nickname`, `role`, `strength` and `symbol`.
Multiple attributes can be specified in the same query. This feature is case insensitive.

Additional query arguments `age_more_than` and `age_less_than` have been implemented for more precise querying.

To fetch a character by ID, see [ Get character by ID](#get-character-by-id)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Sorting

Additionally, it is possible to sort the results by a certain attribute, e.g.:

    `.../api/characters?sort_by=house&sort_desc=true`

The default sorting is in **ascending** order.
If desired, the query argument `sort_des` can be passed, which orders the results in **descending** order.
The argument's value is irrelevant: `sort_des=true` and `sort_des=no` will **both result in descending order**.

If `sort_des` is passed without `sort_by`, the results will default to be ordered by ID and in descending order.

If no query arguments were provided, the API will fetch 20 random characters from the database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Request Example

URL: `.../api/characters?house=baratheon&sort_by=role&sort_des=yes&limit=3`

METHOD: `GET`

### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Server: Werkzeug/2.3.7 Python/3.12.2
    Date: Sat, 08 Feb 2025 16:23:38 GMT
    Content-Type: application/json
    Content-Length: 1214
    Connection: close

    [
        {
            "age": 16,
            "animal": "Stag",
            "death": 5,
            "house": "Baratheon",
            "id": 44,
            "name": "Myrcella Baratheon",
            "nickname": null,
            "role": "Princess",
            "strength": "Cunning",
            "symbol": "Crowned Stag"
        },
            and 2 other characters...
    ]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Get character by ID

    .../api/characters/{character_id}

### Request Example

URL: `http://localhost:5432/api/characters/1`

METHOD: `GET`

### Response

    
    HTTP/1.1 200 OK
    Status: 200 OK
    Server: Werkzeug/2.3.7 Python/3.12.2
    Date: Sat, 08 Feb 2025 16:23:38 GMT
    Content-Type: application/json
    Content-Length: 218
    Connection: close

    {
        "age": 25,
        "animal": "Direwolf",
        "death": null,
        "house": "Stark",
        "id": 1,
        "name": "Jon Snow",
        "nickname": "King in the North",
        "role": "King",
        "strength": "Physically strong",
        "symbol": "Wolf"
    }

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Create a new character

This endpoint requires a token provided from [user login](#login-fetch-token).

Use this endpoint to add a character to the database.

Valid character attributes: `age`, `name`, `house`, `animal`, `death`, `nickname`, `role`, `strength` and `symbol`.

Attribute `name` is required, others are optional.
For a full list of attributes and value types, see [Character Data Models](#character).


### Request

URL: `.../api/characters`

METHOD: `POST`

HEADERS: 

    "Authorization": "your-token"

BODY:

    {
        "id": 51,
        "name": "character-name",
        "house": "character-house",
        "role": "character-role",
        "age": 28,
        ...
    }

### Response

    HTTP/1.1 201 Created
    Status: 201 Created
    Server: Werkzeug/2.3.7 Python/3.12.2
    Date: Sat, 08 Feb 2025 16:23:38 GMT
    Content-Type: application/json
    Content-Length: 185
    Connection: close

    {
        "name": "character-name",
        "house": "character-house",
        "role": "character-role",
        "age": 28,
        ...
    }

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Update a character

This endpoint requires a token provided from [user login](#login-fetch-token).

Use this endpoint to update a character's data in the database.

### Request

URL: `.../api/characters/{character_id}`

METHOD: `PUT`

HEADERS: 

    "Authorization": "your-token"

BODY:

    {
        "nickname": "updated-character-nickname",
        "age": 29,
        ...
    }

### Response

    HTTP/1.1 200 OK
    Status: 200 OK
    Server: Werkzeug/2.3.7 Python/3.12.2
    Date: Sat, 08 Feb 2025 16:23:38 GMT
    Content-Type: application/json
    Content-Length: 196
    Connection: close

    {
        "id": 51,
        "name": "character-name",
        "nickname": "updated-character-nickname",
        "age": 29,
        "house": "character-house",
        ...
    }

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Delete a Character

This endpoint requires a token provided from [user login](#login-fetch-token).

Use this endpoint to delete a character from the database.

### Request

URL: `.../api/characters/{character_id}`

METHOD: `DELETE`

HEADERS: 

    "Authorization": "your-token"

### Response

    HTTP/1.1 204 No Content
    Status: 204 No Content
    Server: Werkzeug/2.3.7 Python/3.12.2
    Date: Sat, 08 Feb 2025 16:23:38 GMT
    Content-Type: application/json
    Connection: close

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Data Models

## User

    {
        "id": 1,  # int
        "username": "your-username",  # str
        "password": "your-password",  # str
        "created_at": 2025-02-08 18:39:31.521848+01  # timestamp with time zone
    }

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Character

    {
        "id": 2,  # int
        "age": 24,  # int
        "death": 8,  # int of what season character died, null if didn't
        "animal": "Dragon",  # str
        "house": "Targaryen",  # str
        "name": "Daenerys Targaryen",  # str
        "nickname": "Mother of Dragons",  # str
        "role": "Queen",  # str
        "strength": "Cunning",  # str
        "symbol": "Dragon"  # str
    }


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contributing

Contributions are what makes the open source community such an amazing place to learn, inspire, and create.
Any contributions are **greatly appreciated**.

If you have a suggestion that would make this app better, please fork the repo and create a pull request.
You can also simply open an issue with the tag "enhancement", or [contact me](#contact) via email.

Don't forget to give the project a star!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Thanks a lot!**

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Top contributors:

<a href="https://github.com/Tombunzel/webeetGotAssignment/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Tombunzel/webeetGotAssignment" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

Tom Bunzel - bunzel.tom@gmail.com

Project Link: [https://github.com/Tombunzel/webeetGotAssignment](https://github.com/Tombunzel/webeetGotAssignment)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Tombunzel/webeetGotAssignment.svg?style=for-the-badge
[contributors-url]: https://github.com/Tombunzel/webeetGotAssignment/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Tombunzel/webeetGotAssignment.svg?style=for-the-badge
[forks-url]: https://github.com/Tombunzel/webeetGotAssignment/forks
[stars-shield]: https://img.shields.io/github/stars/Tombunzel/webeetGotAssignment.svg?style=for-the-badge
[stars-url]: https://github.com/Tombunzel/webeetGotAssignment/stargazers
[issues-shield]: https://img.shields.io/github/issues/Tombunzel/webeetGotAssignment.svg?style=for-the-badge
[issues-url]: https://github.com/Tombunzel/webeetGotAssignment/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/bunzeltom/
[Flask]: https://img.shields.io/badge/Flask-069486?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/stable/
[SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-D61F00?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-336790?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[JWT]: https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=FF3E00
[JWT-url]: https://jwt.io/
