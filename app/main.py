from  flask import Flask
from routes.users import users_routes_bp

app=Flask(__name__)
app.register_blueprint(users_routes_bp, url_prefix='/users')


if __name__== '__main__':
    app.run(debug=True)