from flask import Blueprint,jsonify, request,abort
from flask_restx import Api, Resource, fields
from services.user_services import create_user,get_user,get_all_users

users_routes_bp =Blueprint('users',__name__)

api = Api(users_routes_bp, version = "1.0", title='Users API', description='API for and management users')

# Model for Swagger documentation
users_routes_model = api.model('Users', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required = True, description='The username'),
    'email': fields.String(required = True, description='The user email'),
    'password': fields.String(required = True, description='The password')
})

@api.route('/users')
class UserResource(Resource):
    @api.expect(users_routes_model)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Bad Request')
    def post(self):
        data = request.json
        response, status_code = create_user(data)
        return response, status_code

    def get(self):
        """Get all users."""
        users = get_all_users()
        return users, 200

@api.route('/users/<int:user_id>')
@api.doc(params={'user_id': 'The user id'})
class User(Resource):
    @api.marshal_with(users_routes_model)
    def get(self, user_id):
        user = get_user(user_id)
        if not user:
            api.abort(404)
        return user, 200
