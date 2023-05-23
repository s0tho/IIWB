from flask import Flask
from db import Database

app = Flask(__name__)

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