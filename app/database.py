from config import cursor

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
        user INT,
        FOREIGN KEY (user) REFERENCES users(id)

    )
""")

cursor.close()
