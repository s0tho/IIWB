from flask import Flask
from back.db import Database
from back.routes.api import api as api_v0
from back.routes.v1 import api as api_v1

app = Flask(__name__)
app.register_blueprint(api_v0, url_prefix='/api')
app.register_blueprint(api_v1, url_prefix='/v1')

db = Database("localhost", "admin", "password", "users")
db.connect()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/users")
def get_users():
    test = db.read()
    
    users = list()
    for row in test:
        users.append(row['doc'])
    return users

if __name__ == "__main__":
    app.run()