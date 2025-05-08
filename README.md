# Simple Notes App

## Overview


## Features
- **User Authentication**
- **Note Management**
- **Translation Service**
- **Data Persistence**
- **Responsive UI**

## Technical Stack
- **Language**: Python 3.11
- **Framework**: FastAPI for REST API
- **API Documentation**: OpenAPI (accessible at `/docs`)
- **Database**: SQLite for persistent storage
- **Front-End**: WIP
- **Version Control**: GitHub
- **Containerization**: Docker and Docker Compose
- **Authentication**: JWT (python-jose) with bcrypt (passlib)
- **Translation**: Deep Translate API


## Quality Report

### Maintainability
- **Code Style**: Code follows PEP8 standard ensured by Flake8 on CI
- **Maintainability Index**: Each file on application folder has this index higher than 80

```bash
╰─ poetry run radon mi app/ -s
app/main.py - A (100.00)
app/__init__.py - A (100.00)
app/api/auth.py - A (81.44)
app/api/notes.py - A (87.84)
app/api/__init__.py - A (100.00)
app/core/database.py - A (100.00)
app/core/security.py - A (84.25)
app/db/__init__.py - A (100.00)
app/dependencies/auth.py - A (93.57)
app/models/notes.py - A (100.00)
app/models/translations.py - A (100.00)
app/models/user.py - A (100.00)
app/schemas/note.py - A (100.00)
app/schemas/user.py - A (100.00)
app/services/note_service.py - A (80.73)
app/services/translation_service.py - A (84.66)
```

- **Modularity**: Code organized into reusable modules (`api`, `core`, `models`, `schemas`, `services`, `templates`).
- **Documentation**: Coverage is 94.1%, also has CI check enabled to not fall below 90%

```bash
╰─ poetry run docstr-coverage app/
Checking python files: 100%|█████████████████████████████████████████████████████████████████████████████████| 16.0/16.0 [00:00<00:00, 163files/s]

File: "/mnt/c/Users/muhammad/sqrs-project/simple_notes_app/app/main.py"
 - No docstring for `root`
 - No docstring for `register`
 - No docstring for `notes`
 Needed: 4; Found: 1; Missing: 3; Coverage: 25.0%


Overall statistics for 16 files (3 files are empty):
Needed: 51  -  Found: 48  -  Missing: 3
Total coverage: 94.1%  -  Grade: Excellent
```

### Reliability
- **Test Coverage**: Unit tests cover 91% lines of code

Part of the command `poetry run pytest --cov=app --cov-report=term-missing`:

```
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
app/__init__.py                    0      0   100%
app/api/__init__.py                0      0   100%
app/api/auth.py                   29      2    93%   33, 37
app/api/notes.py                  32      2    94%   86, 113
app/core/database.py              24      0   100%
app/core/security.py              31      4    87%   13, 62, 83-84
app/db/__init__.py                 0      0   100%
app/dependencies/auth.py          13      2    85%   28, 31
app/main.py                       24      9    62%   20-22, 27-29, 34-36
app/models/notes.py               10      0   100%
app/models/user.py                 8      0   100%
app/schemas/note.py               14      0   100%
app/schemas/user.py               13      0   100%
app/services/note_service.py      27      2    93%   46, 69
------------------------------------------------------------
TOTAL                            225     21    91%
```

- **Test Pass Rate**: 100%, ensured by CI
- **Error Handling**: We implemented rollback mechanism if any errors occur, see detailed in `app/core/database.py`
- **Atomic Transactions**: SQLite transactions managed via SQLAlchemy, ensuring data consistency.

### Performance

To analyze performance of our application we used Locust. We set number of concurrent users to 20 to see if minimal amount of users requirement can be satisfied:



### Security

- We used `bandit` to check if we have any critical vulnerabilities, also used it on CI to identify on push if any
- Passwords hashed using `bcrypt`
- Ensured that we have no user sensitive data leakage on API responses

## Project Structure
```
.
├── .vscode
│   ├── launch.json
│   └── settings.json
├── simple_notes_app
│   ├── app
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── notes.py
│   │   ├── core
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── db
│   │   │   ├── __init__.py
│   │   │   └── notes.db
│   │   ├── dependencies
│   │   │   └── auth.py
│   │   ├── models
│   │   │   ├── notes.py
│   │   │   ├── translations.py
│   │   │   └── user.py
│   │   ├── schemas
│   │   │   ├── note.py
│   │   │   └── user.py
│   │   ├── services
│   │   │   ├── note_service.py
│   │   │   └── translation_service.py
│   │   ├── templates
│   │   │   ├── login.html
│   │   │   ├── notes.html
│   │   │   └── register.html
│   │   ├── __init__.py
│   │   └── main.py
│   ├── performance
│   │   └── locustfile.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_api.py
│   ├── .coverage
│   ├── .env
│   ├── .env.example
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── poetry.lock
│   └── pyproject.toml
├── .flake8
├── .gitignore
├── LICENSE
└── README.md
```


## Setup and Installation

### Prerequisites

You can run the project using **either Docker** or **Python 3.11 + Poetry**.

* **Option 1: Docker**:

  * Docker
  * Docker Compose

* **Option 2: Poetry**:

  * Python 3.11
  * Poetry (install via `pip install poetry`)

---

### Steps


1. **Clone the Repository**:

```bash
git clone https://github.com/TheAnushervon/SQRS_Project-Simple-Notes-App.git
cd SQRS_Project-Simple-Notes-App/simple_notes_app
```

---

### Option 1: Run with Docker

2. **Build and Run the Application**:

```bash
docker-compose up --build
```

---

### Option 2: Run with Python 3.11 + Poetry

2. **Install Dependencies**:

```bash
poetry install --no-root
```

3. **Run the Application**:

```bash
poetry run uvicorn app.main:app --reload
```

4. **Run the front end (separate terminal)**

```bash
PYTHONPATH=. poetry run streamlit run streamlit_app/Home.py --server.address=0.0.0.0
```


### Access the Application

- Open `http://localhost:8000` in your browser.
- Register a new user, log in, and manage notes at `/notes`.
- View API documentation at `http://localhost:8000/docs`.


## API Documentation
The REST API is documented using OpenAPI, accessible at `http://localhost:8000/docs`. Key endpoints include:
- `POST /signup`: Register a new user.
- `POST /login`: Authenticate and receive a JWT token.
- `GET /api/notes`: Retrieve all notes for the authenticated user.
- `POST /api/notes`: Create a new note.
- `PUT /api/notes/{note_id}`: Update a note.
- `DELETE /api/notes/{note_id}`: Delete a note.

## Team and Contribution

Anushervon Qodirzoda | a.qodirzoda@innopolis.university
  
- Database
- API: Notes, Authorization
- Docker

Iliays Dzhabbarov | i.dzhabbarov@innopolis.university

- API: Translation
- Frontend on Streamlit
- Testing: UI

Muhammad Allayarov | m.allayarov@innopolis.university

- Testing: Unit, Mutation, Performance
- Documentation