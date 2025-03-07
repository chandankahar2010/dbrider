# DB Rider Integration for API Testing

## Overview
This project uses **DB Rider** for database testing in FastAPI applications. It helps in setting up, managing, and cleaning up test datasets before and after test execution.

## Features
- Automated dataset handling using `@dataset` decorator.
- Supports both **dataset_paths** (JSON/YAML files) and **dataset_providers** (Python functions).
- Ensures database consistency before and after tests.
- Uses **FastAPI TestClient** for API testing.
- Supports Peewee ORM with PostgreSQL.

---

## Installation

Make sure you have Python installed, then install the dependencies:

```sh
pip install fastapi sqlalchemy dbrider faker pytest peewee
```

---

## Database Configuration

The test database is configured as follows:

```python
DATABASE_URL = {
    "database": "your database name",
    "user": "postgres",
    "password": "you password",
    "host": "localhost",
    "port": 5432
}
```

Using Peewee ORM:

```python
from playhouse.postgres_ext import PostgresqlDatabase

peewee_db = PostgresqlDatabase(**DATABASE_URL)
```

---

## Using `@dataset` Decorator

### Example with `dataset_providers`

```python
from dbrider.decorator import dataset
from fastapi.testclient import TestClient
from app.main import app

def test_dataset():
    return {
        "users": [
            {"id": 1, "username": "testuser", "email": "test@example.com", "password": "test123"}
        ]
    }

@dataset(dataset_providers=[test_dataset], cleanup_before=True, cleanup_after=True)
def test_signup():
    client = TestClient(app)
    signup_data = {"username": "chandan", "email": "chandan@example.com", "password": "chandan123"}
    response = client.post("/signup", json=signup_data)
    print(response.status_code, response.json())
```

### Example with `dataset_paths`

```python
@dataset(dataset_paths=["tests/data/user_data.json"], cleanup_before=True, cleanup_after=True)
def test_signup_with_file():
    client = TestClient(app)
    signup_data = {"username": "rohan", "email": "rohan@example.com", "password": "rohan123"}
    response = client.post("/signup", json=signup_data)
    print(response.status_code, response.json())
```

---

## Running the Tests
run manually:

```sh
python -m app.routes.test_signup
```

---

## Cleanup Strategy
- `cleanup_before=True`: Clears the dataset before test execution.
- `cleanup_after=True`: Clears the dataset after test execution.

This ensures that the test database remains clean and does not affect other test runs.

---

## Troubleshooting
- **404 Not Found**: Check if the API endpoint exists in `app/main.py`.
- **400 Bad Request**: Verify if test data is correct or if the user already exists.
- **Database Connection Issues**: Ensure PostgreSQL is running and credentials are correct.

---

## Author
**Chandan Kahar**

---