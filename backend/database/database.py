import os
from pathlib import Path
import dotenv
from abc import ABC, abstractmethod
import psycopg2

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / ".env")


class Database(ABC):
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def connect_to_db(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_db()
        self.cursor = self.connection.cursor()

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


class PgDatabase(Database):
    def __init__(self) -> None:
        self.driver = psycopg2
        super().__init__(self.driver)

    def connect_to_db(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )


users = "users"
user_recipes = "user_recipes"
global_recipes = "global_recipes"
meal_plans = "meal_plans"
meal_plan_recipes = "meal_plan_recipes"


def create_tables():
    with PgDatabase() as db:
        db.cursor.execute(
            f"""CREATE TABLE {users} (
			id SERIAL PRIMARY KEY,
			created_date TIMESTAMPZ DEFAULT NOW(),
			username VARCHAR(20) UNIQUE NOT NULL,
			password VARCHAR(100) NOT NULL,
			email VARCHAR(30) NOT NULL,
			);
		"""
        )
        db.connection.commit()
        print("Users table created successfully...")

        db.cursor.execute(
            f"""CREATE TABLE {user_recipes} (
			id SERIAL PRIMARY KEY,
			user_id INTEGER REFERENCES users(id)
			created_date TIMESTAMPZ DEFAULT NOW(),
			url TEXT NOT NULL,
			name VARCHAR(100) NOT NULL,
			ingredients JSONB NOT NULL,
			instructions JSONB NOT NULL
			);
		"""
        )
        db.connection.commit()
        print("user_recipes table created successfully...")

        db.cursor.execute(
            f"""CREATE TABLE {user_recipes} (
			id SERIAL PRIMARY KEY,
			user_id INTEGER REFERENCES users(id)
			created_date TIMESTAMPZ DEFAULT NOW(),
			url TEXT NOT NULL,
			name VARCHAR(100) NOT NULL,
			ingredients JSONB NOT NULL,
			instructions JSONB NOT NULL,
			default_portion INTEGER DEFAULT 2
			);
		"""
        )
        db.connection.commit()
        print("user_recipes table created successfully...")

        db.cursor.execute(
            f"""CREATE TABLE {meal_plans} (
			id SERIAL PRIMARY KEY,
			user_id INTEGER REFERENCES users(id)
			created_date TIMESTAMPZ DEFAULT NOW(),
			duration INTEGER DEFAULT 7,
			name VARCHAR(100) NOT NULL,
			);
		"""
        )
        db.connection.commit()
        print("meal_plans table created successfully...")

        db.cursor.execute(
            f"""CREATE TABLE {meal_plan_recipes} (
			meal_plan_id INTEGER REFERENCES meal_plans(id),
			recipe_id INTEGER REFERENCES user_recipes(id),
			PRIMARY KEY(meal_plan_id, recipe_id)
			);
		"""
        )
        db.connection.commit()
        print("meal_plans table created successfully...")
