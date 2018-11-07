import os
from flask import Flask
from flask import request
from flask import jsonify
import json
import pymongo

from model.user import User
from model.daouser import DAOUser

# App definition
app = Flask(__name__)

# MongoDB configuration
MONGODB_URI = 'mongodb://user:user123@ds024548.mlab.com:24548/apolo-mongodb'
COLLECTION_NAME = 'users'

# DAO user
daouser = DAOUser(MONGODB_URI, COLLECTION_NAME)

@app.route('/')
def index():
    data = {}
    data['status'] = 'OK'
    data['ruta'] = request.url
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/about')
def about():
    data = {}
    data['status'] = 'OK'
    data['author'] = 'Pedro Manuel Gomez-Portillo Lopez'
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/insert')
def insert():
    new_user = parse_arguments_to_user( request.args )
    status = daouser.insert(new_user)

    result = {}
    result['status'] = status
    result['message'] = 'On adding user with email {} '.format(new_user.email)

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.route('/update')
def update():
    user = parse_arguments_to_user( request.args )
    status = daouser.update(user)

    result = {}
    result['status'] = status
    result['message'] = 'On updating user with email {} '.format(user.email)

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.route('/delete')
def delete():
    user = parse_arguments_to_user( request.args )
    status = daouser.delete(user)

    result = {}
    result['status'] = status
    result['message'] = 'On deleting user with email {} '.format(user.email)

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.route('/readall')
def readall():
    users = daouser.readAll()
    resp = jsonify(users)
    resp.status_code = 200
    return resp

@app.route('/find')
def find():
    email = str(request.args.get('email'))
    instrument = str(request.args.get('instrument'))

    if email == 'None':
        email = ''
    if instrument == 'None':
        instrument = ''

    user = User(email, instrument)

    if user.empty():
        status = 'USER_EMPTY'
    else:
        status = daouser.find(user)

    result = {}
    result['status'] = status
    result['message'] = 'On find user ' + json.dumps(user.toDict())

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found():
    msg = {}
    msg['status'] = 404
    msg['message'] = 'URL {} not found'.format(request.url)

    resp = jsonify(msg)
    resp.status_code = 404
    return resp

def parse_arguments_to_user(args):
    email = str(request.args.get('email'))
    instrument = str(request.args.get('instrument'))

    if email == 'None':
        email = 'jhon@doe.com'
    if instrument == 'None':
        instrument = 'triangle'

    return User(email, instrument)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
