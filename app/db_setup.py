from date_conversions import create_connection

connection = create_connection()
cursor = connection.cursor()

cursor.execute("""

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(60),
    email VARCHAR(120)
)
""")

cursor.execute("""
    CREATE TABLE events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(120),
        description VARCHAR(255),
        start_time DATETIME,
        end_time DATETIME,
        location VARCHAR(255),
        email VARCHAR(120),
    )
""")

cursor.execute("""
CREATE TABLE bookings (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
event_id INT,
booking_time DATETIME DEFAULT NOW(),
FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE

)
""")

cursor.close()
