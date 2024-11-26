import mysql.connector
from datetime import datetime
from mysql.connector import Error

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='    ',  # Replace with your MySQL password
            database='events_management'  # Replace with your database name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


from datetime import datetime


def convert_to_mysql_datetime(iso_datetime):
    """
    Convert an ISO 8601 datetime string (e.g., '2024-11-26T17:06:39.104Z') to MySQL datetime format (YYYY-MM-DD HH:MM:SS).
    """
    # Remove 'Z' (UTC) and replace with '+00:00' for correct parsing
    iso_datetime = iso_datetime.replace("Z", "+00:00")

    # Parse the ISO datetime string into a Python datetime object
    datetime_obj = datetime.fromisoformat(iso_datetime)

    # Convert to MySQL format: 'YYYY-MM-DD HH:MM:SS'
    return datetime_obj.strftime('%Y-%m-%d %H:%M')


def mysql_to_iso(mysql_datetime):
    """Converts MySQL DATETIME to ISO format"""
    try:
        dt = datetime.strptime(mysql_datetime, '%Y-%m-%d %H:%M:%S')
        return dt.isoformat()
    except ValueError as e:
        return None


