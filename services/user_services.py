from app.config import create_connection

connection = create_connection()
cursor = connection.cursor()

#create a new user
def create_user(data):
    """Query to insert data of new user into the users table"""
    query="""
    INSERT INTO users (username, email, password) 
    VALUES (%s, %s, %s)"""

    try:
        cursor.execute(query, (data['username'], data['email'], data['password']))
        connection.commit()  # Commit the changes to the database

        # Return the user data along with a 201 status code
        return {"message": "User created successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 400

#fetch a user using user id
def get_user(user_id):
    """Query to get user information from the users table"""
    query = "SELECT id,username, email, password FROM users WHERE id = %s"

    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user
    except Exception as e:
        return f"Error fetching user: {e}", 500


# FEtch all the users in the dtabse
def get_all_users():
    """Query to get all user information from the users table"""
    query = "SELECT id, username, email,password FROM users"
    connection = create_connection()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            users = cursor.fetchall()
            if not users:
                return {"No users found"}, 404
            return users
    except Exception as e:
        return {f"Error fetching users: {e}"}, 504

def update_user(user_id, new_username, new_password, new_email):

    update_query = "UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s"

    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(update_query, (user_id, new_username, new_email, new_password))
            connection.commit()
            return {"message": "User updated successfully"}, 200
    except Exception as e:
        return {"message": str(e)}, 400

def delete_user(user_id):
    """Query to get user information from the users table"""
    query = "SELECT * FROM users WHERE id = %s"

    """Query to delete user information from the users table"""
    delete_query = "DELETE FROM users WHERE id = %s"

    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            if user:
                cursor.execute(delete_query, (user['username'], user['email']))
                connection.commit()
                return {"message": "User deleted successfully"}, 200
            else:
                return {"message": "User not found"}, 404
    except Exception as e:
        return {"message": str(e)}, 400
