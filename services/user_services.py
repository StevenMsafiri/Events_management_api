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