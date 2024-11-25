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
        connection.rollback()

        # Return the user data along with a 201 status code
        return {"message": "User created successfully"}, 201
    except Exception as e:
        connection.rollback()
        connection.close()
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
        connection.rollback()
        connection.close()
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
        connection.rollback()
        connection.close()
        return {f"Error fetching users: {e}"}, 504


def delete_user(id):
    """Delete a user from the events table using the event ID."""
    query = "DELETE FROM users WHERE id = %s"

    try:
        cursor.execute(query, (id,))
        connection.commit()

        # Check if any row was affected (if no rows, return an error)
        if cursor.rowcount == 0:
            return f"No user found with ID {id}", 404
        return f"User {id} deleted successfully", 200
    except Exception as e:
        connection.rollback()  # Ensure rollback on error
        connection.close()
        return f"Failed to delete event: {e}", 500

def update_user(id, username, email, password):
    """Update a user in the users table based on the user ID."""
    search_query = "SELECT * FROM users WHERE id = %s"
    update_query = """UPDATE users 
                      SET username = %s, email = %s, password = %s 
                      WHERE id = %s"""

    try:
        # First, check if the user exists
        cursor.execute(search_query, (id,))
        event = cursor.fetchone()

        if not event:
            return f"No user found with ID {id}", 404
        # If event exists, update it
        cursor.execute(update_query, (username, email, password, id))
        connection.commit()

        if cursor.rowcount == 0:
            return f"No changes made to user {id}", 304  # No content modified

        return f"User {id} updated successfully", 200
    except Exception as e:
        connection.rollback()  # Ensure rollback on error
        connection.close()
        return f"Failed to update user: {e}", 500
