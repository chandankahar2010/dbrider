from pathlib import Path
from fastapi.testclient import TestClient
from ..main import app
from ..database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbrider.decorator import dataset
from ..models import User
from faker import Faker
from dbrider import DataSetConfig, DataSetHandler, JsonDataSetLoader, DatabaseExecutor, setup_db_rider
from playhouse.postgres_ext import PostgresqlDatabase
from dbrider.decorator import dataset
from ..config import Config

base_url = "http://127.0.0.1:9001/"

DATABASE_URL = {
    "database": Config.DB_NAME,
    "user": Config.DB_USER,
    "password": Config.DB_PASSWORD,
    "host": Config.DB_HOST,
    "port": Config.DB_PORT
}
peewee_db = PostgresqlDatabase(**DATABASE_URL)
executor = DatabaseExecutor(peewee_db)

loader = JsonDataSetLoader()

setup_db_rider(peewee_db,database_executor=executor,dataset_loader=loader,dataset_matcher=None)

client = TestClient(app)
fake = Faker()

# code for using dataset_paths
@dataset(dataset_paths=["user_data.json"], cleanup_before=False, cleanup_after=False)
def test_signup():
    signup_data = {
        "username": "chandan",
        "email": "chandan@example.com",
        "password": "chandan123"
    }

    response = client.post(f"{base_url}api/signup/", json=signup_data)

    print('Response:', response.status_code, response.json())

    if response.status_code == 200:
        print("Signup successful:", response.json())
    elif response.status_code == 400:
        print("Signup failed: User Already Exists.")
    elif response.status_code == 404:
        print(f"ERROR: Endpoint '/signup' not found! Check route path.")
    else:
        print(f"Unexpected response: {response.status_code}, {response.json()}")


# code for using dataset providers
def test_dataset():
    return {
        "users": [
            {
                "id": 6,
                "username": "rohan",
                "email": "rohan@example.com",
                "password": "rohan123"
            }
        ]
    }

@dataset(dataset_providers=[test_dataset], cleanup_before=False, cleanup_after=False)
def test_signup():
    signup_data = {
        "username": "chandan",
        "email": "chandan@example.com",
        "password": "chandan123"
    }

    response = client.post(f"{base_url}api/signup/", json=signup_data)

    print('Response:', response.status_code, response.json())

    if response.status_code == 200:
        print("Signup successful:", response.json())
    elif response.status_code == 400:
        print("Signup failed: User Already Exists.")
    elif response.status_code == 404:
        print(f"ERROR: Endpoint '/signup' not found! Check route path.")
    else:
        print(f"Unexpected response: {response.status_code}, {response.json()}")
        
if __name__ == "__main__":
    print("Running test_signup directly...")
    test_signup()
    print("Test completed successfully!")



# for dataset_providers
"""
if __name__ == "__main__":
    print("Running test_signup directly...")
    try:
        fake = Faker()

        # Function to generate fake users
        def generate_users():
            return {
                "users": [
                    {
                        "id": i,
                        "username": fake.user_name(),
                        "email": fake.email(),
                        "password": fake.password()
                    } for i in range(1, 6)
                ]
            }

        loader = JsonDataSetLoader()

        config = DataSetConfig(
            dataset_paths=None,
            dataset_providers=[generate_users],
            dataset_variables=None,
            cleanup_before=True,
            cleanup_after=False,
            cleanup_tables=None,
            execute_scripts_before=None,
            execute_statements_before=None,
            execute_scripts_after=None,
            execute_statements_after=None,
            expected_dataset_paths=None,
            expected_dataset_providers=None,
            expected_dataset_matchers=None
        )

        dataset_directory = Path(".")

        handler = DataSetHandler(config, loader, executor, None, dataset_directory)
        handler.execute_before()

        handler.execute_after()

        print("Test completed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")
"""



# for Dataset paths
"""
if __name__ == "__main__":
    print("Running test_signup directly...")
    try:
        fake = Faker()
    
        dataset_paths = ["routes/user_data.json"]

        loader = JsonDataSetLoader()

        config = DataSetConfig(
            dataset_paths=dataset_paths,
            dataset_providers=None,
            dataset_variables=None,
            cleanup_before=True,
            cleanup_after=True,
            cleanup_tables=None,
            execute_scripts_before=None,
            execute_statements_before=None,
            execute_scripts_after=None,
            execute_statements_after=None,
            expected_dataset_paths=None,
            expected_dataset_providers=None,
            expected_dataset_matchers=None
        )

        dataset_directory = Path("/home/hexa/Desktop/DB Rider FastApi/app")

        handler = DataSetHandler(config, loader, executor, None, dataset_directory)
        handler.execute_before()

        handler.execute_after()

        print("Test completed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")
"""


# for using api run test dataset
"""
if __name__ == "__main__":
    print("Running test_signup directly...")
    try:
        fake = Faker()
        client = TestClient(app)

        # Function to generate fake users
        def test_dataset():
            return {
                "users": [
                    {
                        "id": 1,
                        "username": "newuser",
                        "email": "newuser@example.com",
                        "password": "newpass123"
                    }
                ]
            }

        loader = JsonDataSetLoader()

        config = DataSetConfig(
            dataset_paths=None,
            dataset_providers=[test_dataset],
            dataset_variables=None,
            cleanup_before=True,
            cleanup_after=False,
            cleanup_tables=None,
            execute_scripts_before=None,
            execute_statements_before=None,
            execute_scripts_after=None,
            execute_statements_after=None,
            expected_dataset_paths=None,
            expected_dataset_providers=None,
            expected_dataset_matchers=None
        )

        dataset_directory = Path(".")

        handler = DataSetHandler(config, loader, executor, None, dataset_directory)
        handler.execute_before()

        signup_data = {
            "username": "chandan",
            "email": "chandan@example.com",
            "password": "chandan123"
        }
        response = client.post("http://127.0.0.1:9001/api/signup/", json=signup_data)

        if response.status_code == 200:
            print('success----------->',response.json())
        elif response.status_code == 400:
            print("Signup failed: User Already Exists. Check request data.")
        else:
            print(f"Unexpected response: {response.status_code}, {response.json()}")

        handler.execute_after()

        print("Test completed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")

"""