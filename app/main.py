from  flask import Flask

app=Flask(__name__)


@app.route('/')
def home():
    return "This is an Event Management Api"

if __name__== '__main__':
    app.run(debug=True)