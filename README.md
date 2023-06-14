# FastAPI-React project template

This is a project template for building a web application using the FastAPI backend framework and React frontend library. It provides a basic structure and setup to help you get started quickly with developing your own FastAPI-React project.


## Features

- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- React: A JavaScript library for building user interfaces, allowing you to create interactive components and manage the application's state efficiently.
- PostgreSQL: A powerful open-source relational database system
- Docker: Simplifies the deployment process by encapsulating the application and its dependencies into containers.


## Prerequisites

To use this template, make sure you have the following installed on your system:

- Python 3.7 or higher
- Node.js and npm
- Docker (optional, for containerized deployment)
- PostgreSQL (optional, for using a database)


## Getting started

1. Backend Setup
    -  Navigate to `app` directory <br>`cd backend/app/`

    - Create an .env file with the following environment<br>
    `TOKEN = `<br>
    `ALGORYTM = ` <br>
    `DB_USER = `<br>
    `DB_PASS = `<br>
    `DB_HOST = `<br>
    `DB_NAME = ` <br>
    `DATABASE_URL = `<br>
    

    -  Create a virtual environment <br>`python3 -m venv venv`

    -  Activate the virtual environment <br> `source venv/bin/activate`

    - Install the dependencies <br> `pip install -r ../requirements.txt`
    
    - Pre-commit instalation <br> `pre-commit install`

    - Run server <br> `uvicorn main:app --reload`

2. Frontend Setup
    -  Navigate to `frontend` directory <br>`cd frontend/`

    - Install the dependencies: <br> `npm install`

    - Run the frontend server: <br> `npm start`


3. Docker

    - While in the main project dir in which the `docker-compose.yml` is<br>
    `docker compose up --build -d`

    - to stop the container <br>
    `docker compose down`
