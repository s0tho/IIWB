from http import HTTPStatus
from flask import Blueprint, request
from back.Models import ApiModel
from back.Schemas import ApiSchema

from back.db import Database


api = Blueprint('api_v1', __name__)


db = Database("localhost", "admin", "password", "users")
db.connect()


@api.route('/')
def index():
    return "This is an example app"

@api.route("/users")
def get_users():
    test = db.read()
    
    users = list()
    for row in test:
        users.append(row['doc'])
    return users

@api.route('/usermp', methods=['POST'])
def addusermp():
    _json = request.json
    
    _dbe = db.inst['moonphase']
    try:
        value = _dbe[str(_json["_id"])]
        return "Value skipped already exists in database."
    except:
        print("Value does not exist")
        db.write_moonphase(_json)
        return "Value does not exist, and is registered."
    return "Error 500"
   

@api.route('/userbyidmp/<id>', methods=['GET'])
def getuserbyidmp(id):
    dbe = db.inst['moonphase']
    try:
        value = dbe[str(id)]
    except:
        value = {
            "_id": None
        }
    return value

@api.route('/userbyidmp/<id>', methods=['PUT'])
def updateuserdata(id):
    dbe = db.inst['moonphase']
    try:
        value = dbe.get(id)
        value.update(request.json)
        dbe.save(doc=value)
    except Exception() as e:
        value = {
            "_id": None
        }
        print(e)
    return value

@api.route('/users/<id>/timemonitor', methods=['GET'])
def getusertimemonitor(id):
    dbe = db.inst['timemonitor']
    try:
        # value = dbe[str(id)]
        print(id)
        mango = { "userid": id }
        value = dbe.find()
    except:
        value = {
            "_id": None
        }
    return value

@api.route('/timemonitor/users', methods=['POST'])
def createusertimemonitor():

    _json = request.json
    
    _dbe = db.inst['timemonitor']
    try:
        value = _dbe[str(_json["_id"])]
        return "Value skipped already exists in database."
    except:
        print("Value does not exist")
        db.write_timemonitor(_json)
        return "Value does not exist, and is registered."
    return "Error 500"

@api.route('/timemonitor/users/<id>', methods=['PUT'])
def updateusertimemonitor(id):
    dbe = db.inst['timemonitor']
    try:
        value = dbe.get(id)
        value.update(request.json)
        dbe.save(doc=value)
    except Exception() as e:
        value = {
            "_id": None
        }
        print(e)
    return value