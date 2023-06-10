from http import HTTPStatus
from flask import Blueprint, jsonify, request
from back.Models import ApiModel
from back.Schemas import ApiSchema
from back.db import Database


api = Blueprint('api_v1', __name__)


db = Database("localhost", "admin", "DoAXvxZ_VbPKI", "users")
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

@api.route('/user/<id>', methods=['POST'])
def insertUserInfos(id):
	print(id)
	dbe = db.inst['users']
	mango = {
			"selector": {
				"userid": str(id)
			},
			"limit": 1
		}
	print(mango)
	value = []
	for row in dbe.find(mango):
		value.append(row)

	if(len(value) <= 0):
		_json = request.json
	
		print("Value does not exist")
		save = db.write_userinfo(_json)
		return save
	else:
		print("Already exist")
	return value

@api.route('/user/<id>', methods=['PUT'])
def updateUserInfos(id):
	dbe = db.inst['users']
	try:
		value = dbe.get(id)
		value.update(request.json)
		dbe.save(value)
	except Exception() as e:
		value = {
		"_id": None
		}
		print(e)
	return value

@api.route('/user/<id>', methods=['get'])
def getUser(id):
	print(id)
	dbe = db.inst['users']
	mango = {
			"selector": {
				"userid": str(id)
			},
			"limit": 1
		}
	print(mango)
	value = []
	for row in dbe.find(mango):
		value.append(row)
	return value

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
		mango = { "userid": str(id) }
		mango = {"selector":{"userid": str(id)},"sort":[{"status.connected":"desc"}]}
		print(mango)
		value = []
		for row in dbe.find(mango):
			value.append(row)
		return value
	except Exception as e:
		print(e)
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
		_id, _rev= db.write_timemonitor(_json)
		c = {'_id': _id, '_rev': _rev}
		d = {**c, **_json}
		return d
	return "Error 500"

@api.route('timemonitor/getspecific', methods=['POST'])
def getspecificentry():
	dbe = db.inst['timemonitor']
	try:
		_j = request.json
		mango = {"selector":{"_id": str(_j['_id'])},"limit": 1, "sort":[{"status.connected":"desc"}]}
		print(mango)
		value = []
		for row in dbe.find(mango):
			value.append(row)
		return value
	except:
		print(e)
		value = {"_id": None}
	return value

@api.route('/timemonitor/users/<id>', methods=['PUT'])
def updateusertimemonitor(id):
	dbe = db.inst['timemonitor']
	try:
		print(dbe)
		value = dbe.get(id)
		value.update(request.json)
		dbe.save(doc=value)
		print(value)
	except Exception() as e:
		value = {
			"_id": None
		}
		print(e)
	return value

@api.route('/poll', methods=['GET'])
def getallpoll():
	dbe = db.inst['poll']
	try:
		rows = dbe.view('_all_docs', include_docs=True)
		data = [row['doc'] for row in rows]
		print(data)
		return data
	except Exception as e:
		print(e)

@api.route('/poll', methods=['POST'])
def insertpoll():
	dbe = db.inst['poll']
	_json = request.json
		
	try:
		value = dbe[str(_json["_id"])]
		return "Value skipped already exists in database."
	except:
		print("Value does not exist")

		_id, _rev = db.write_poll(_json)
		_json['_id'] = _id
		_json['_rev'] = _rev
		return _json
	
	return "Error 500"

@api.route('/poll/<id>', methods=['PUT'])
def updatepoll(id):
	dbe = db.inst['poll']

	try:
		value = dbe.get(id)
		value.update(request.json)
		dbe.save(doc=value)
		print(value)
	except Exception as e:
		print(e)
		value = {
			"_id": None
		}
	return value

@api.route('/clearlogger', methods=['POST'])
def insertClearLogger():
	dbe = db.inst['clearlogger']
	_json = request.json

	try:
		value = dbe[str(_json["_id"])]
		return "Value skipped already exists in database."
	except:
		_id, _rev = db.write_clearlogger(_json)
		_json['_id'] = _id
		_json['_rev'] = _rev
		return _json

@api.route('/messagelogger', methods=['POST'])
def insertMessageLogger():
	dbe = db.inst['messagelogger']
	_json = request.json

	try:
		value = dbe[str(_json["_id"])]
		return "Value skipped already exists in database."
	except:
		_id, _rev = db.write_messagelogger(_json)
		return _json
	
@api.route('/expstore/<id>', methods=['POST'])
def insertExperience(id):
	dbe = db.inst['expstore']
	mango = {
			"selector": {
				f"userid": str(id)
			},
			"limit": 1
		}
	value = []
	for row in dbe.find(mango):
		value.append(row)

	if(len(value) <= 0):
		_json = request.json
	
		print("Value does not exist")
		_id, _rev = db.write_experiencelogger(_json)
		_json['_id'] = _id
		_json['_rev'] = _rev
		return _json
	else:
		print("Already exist")
	return value


@api.route('/expstore/<id>', methods=['PUT'])
def updateExpStore(id):
	dbe = db.inst['expstore']

	try:
		value = dbe.get(id)
		value.update(request.json)
		dbe.save(value)
		print(value)
	except Exception as e:
		print(e)
		value = {
			"_id": None
		}
	return value