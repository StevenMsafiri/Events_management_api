from flask import Flask
from flask_restx import Api
from routes.users import users_ns  # Import the namespace
from routes.events import events_ns # Imports the namespace of events

app = Flask(__name__)
api = Api(app, version="1.0", title="Events Management System", description="APIs for Events management")

# Add the namespace to the API
api.add_namespace(users_ns, path='/users')
api.add_namespace(events_ns, path='/events')

if __name__ == "__main__":
    app.run(debug=True)
