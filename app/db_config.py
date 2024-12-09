from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv("../venv/.env")

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")


# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Connection to MySQL DB successful")

    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection

create_connection()