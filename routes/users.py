from flask import request
from flask_restx import Namespace, Resource, fields
from services.user_services import create_user, get_user, get_all_users, delete_user, update_user

# Define the Namespace
users_ns = Namespace('Users Operations', description='API for user management')

# Model for Swagger documentation
users_model = users_ns.model('Users', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The password'),
})

@users_ns.route('/')
class UserResource(Resource):
    @users_ns.expect(users_model)
    @users_ns.response(201, 'User created successfully')
    @users_ns.response(400, 'Bad Request')
    def post(self):
        """Adds a new user."""
        data = request.json
        response, status_code = create_user(data)
        return response, status_code

    def get(self):
        """Get all users."""
        users = get_all_users()
        return users, 200

@users_ns.route('/<int:user_id>')
@users_ns.doc(params={'user_id': 'The user id'})
class User(Resource):
    @users_ns.marshal_with(users_model)
    def get(self, user_id):
        """Get a specific user by ID."""
        user = get_user(user_id)
        return user

    @users_ns.response(200, "User deleted successfully")
    @users_ns.response(404, "User not found")
    def delete(self, user_id):
        """Delete a specific user by ID."""
        response, status_code = delete_user(user_id)
        if status_code == 404:
            users_ns.abort(404, f"User {user_id} not found")
        return response, status_code

    @users_ns.expect(users_model)
    @users_ns.response(200, "User updated successfully")
    @users_ns.response(404, "User not found")
    def put(self, user_id):
        """Update an existing user."""
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        response, status_code = update_user(user_id, username, email, password)
        if status_code == 404:
            users_ns.abort(404, f"User {user_id} not found")
        return response, status_code
