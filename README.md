# Simple Notes App

## Overview


## Features
- **User Authentication**: 
- **Note Management**: 
- **Translation Service**: 
- **Data Persistence**: 
- **Responsive UI**: 

## Technical Stack
- **Language**: Python 3.11
- **Framework**: FastAPI for REST API
- **API Documentation**: OpenAPI (accessible at `/docs`)
- **Database**: SQLite for persistent storage
- **Front-End**: HTML/CSS/JavaScript templates served by FastAPI
- **Version Control**: GitHub
- **Containerization**: Docker and Docker Compose
- **Authentication**: JWT (python-jose) with bcrypt (passlib)
- **Translation**: Deep Translate API


### Maintainability
- **Code Style**:
- **Maintainability Index**:
- **Modularity**: Code organized into reusable modules (`api`, `core`, `models`, `schemas`, `services`, `templates`).
- **Documentation**:

### Reliability
- **Test Coverage**:
- **Test Pass Rate**:
- **Error Handling**:
- **Atomic Transactions**: SQLite transactions managed via SQLAlchemy, ensuring data consistency.

### Performance
- **API Response Time**:
- **Concurrent Users**:
- **Database Optimization**:

### Security


## Testing
The application has been thoroughly tested to meet quality requirements:
- **Unit Tests**:
- **Integration Tests**:
- **Static Analysis**:
- **Performance Tests**:
- **Security Scans**:

## Project Structure
```
simple_notes_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app setup and entry point
│   ├── api/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py            # Login and signup endpoints
│   │   ├── notes.py           # Note CRUD endpoints
│   │   └── translation.py     # Russian to English translation endpoint
│   ├── core/                  # Configurations and utilities
│   │   ├── __init__.py
│   │   ├── config.py          # Settings (database URL, JWT secret)
│   │   ├── database.py        # SQLite database setup
│   │   └── security.py        # JWT and bcrypt handling
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   └── note.py            # Note model
│   ├── schemas/               # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── user.py            # User schemas
│   │   ├── note.py            # Note schemas
│   │   └── translation.py     # Translation schemas
│   └── services/              # Business logic
│       ├── __init__.py
│       ├── auth_service.py    # Authentication logic
│       ├── note_service.py    # Note management logic
│       └── translation_service.py # Deep Translate API integration
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_auth.py          # Authentication tests
│   ├── test_notes.py         # Note management tests
│   └── test_translation.py   # Translation tests
│
├── .gitignore                 # Git ignore file
├── README.md                  # Project setup guide
├── requirements.txt           # Dependencies (FastAPI, SQLAlchemy, etc.)
├── pyproject.toml             # PEP8 and testing config
├── .flake8                    # Flake8 config for PEP8
└── .bandit                    # Bandit config for security


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

## CI Integration
