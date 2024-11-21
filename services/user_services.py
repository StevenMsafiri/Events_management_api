from app.config import cursor

#create a new user
def create_user(data):
    """Query to insert data of new user into the users table"""
    query="""
    INSERT INTO users (username, email, password) 
    VALUES (%s, %s, %s)"""

    try:
        cursor.execute(query, (data['username'], data['email'], data['password']))
        cursor.connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

#fetch a user using user id
def get_user(user_id):
    """Query to get user information from the users table"""
    query = "SELECT id FROM users WHERE id = %s"

    try:
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.connection.commit()
        if not user:
            return "Invalid id, User not found"
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        return "Error, Failed to fetch user"

    finally:
        cursor.close()

# FEtch all the users inthe dtabse
def get_all_users():
    """Query to get all user information from the users table"""
    query = "SELECT * FROM users"

    try:
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.connection.commit()
        if not users:
            return "No users found"
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return "Error, Failed to fetch users"
    finally:
        cursor.close()