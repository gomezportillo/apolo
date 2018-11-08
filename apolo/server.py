import os
from flask import Flask
from flask import request
from flask import jsonify
from flask_restful import Resource
from flask_restful import Api

import json
import pymongo

from model.user import User
from model.daouser import DAOUser

# App definition
app = Flask(__name__)
api = Api(app)

# MongoDB configuration
MONGODB_URI = 'mongodb://user:user123@ds024548.mlab.com:24548/apolo-mongodb'
COLLECTION_NAME = 'users'

# DAO user
daouser = DAOUser(MONGODB_URI, COLLECTION_NAME)

@app.route('/', methods=['GET'])
def index():
    data = {}
    data['status'] = 'OK'
    data['ruta'] = request.url
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/about', methods=['GET'])
def about():
    data = {}
    data['status'] = 'OK'
    data['author'] = 'Pedro Manuel Gomez-Portillo Lopez'
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/users', methods=['PUT'])
def insert():
    new_user = parse_arguments_to_user( request.form )
    status = daouser.insert(new_user)

    result = {}
    result['status'] = status
    result['message'] = 'On adding user with email {} '.format(new_user.email)

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.route('/users', methods=['POST'])
def update():
    user = parse_arguments_to_user( request.form )
    status = daouser.update(user)

    result = {}
    result['status'] = status
    result['message'] = 'On updating user with email {} '.format(user.email)

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.route('/users', methods=['DELETE'])
def delete():
    user = parse_arguments_to_user( request.form )
    status = daouser.delete(user)

    result = {}
    result['status'] = status
    result['message'] = 'On deleting user with email {} '.format(user.email)

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.route('/users',  methods=['GET'])
def find():
    email = str(request.form['email'])
    instrument = str(request.form['instrument'])

    if email == 'None':
        email = ''
    if instrument == 'None':
        instrument = ''

    user = User(email, instrument)

    status = 'SUCCESS'
    if user.empty():
        status = 'USER_EMPTY'
    else:
        users = daouser.find(user)

    users_json = ''
    for u in users:
        users_json += u
    result = {}
    result['status'] = status
    result['message'] = users

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.route('/readAll', methods=['GET'])
def readall():
    users = daouser.readAll()
    resp = jsonify(users)
    resp.status_code = 200
    return resp

@app.route('/deleteAll', methods=['DELETE'])
def deleteAll():
    status = daouser.deleteAll()

    result = {}
    result['status'] = status
    result['message'] = 'On deleting all users'

    resp = jsonify(result)
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error=None):
    msg = {}
    msg['status'] = 404
    msg['message'] = 'URL {} not found'.format(request.url)

    resp = jsonify(msg)
    resp.status_code = 404
    return resp

@app.errorhandler(405)
def not_allowed(error=None):
    msg = {}
    msg['status'] = 405
    msg['message'] = 'URL {} not allowed from {} HTTP method'.format(request.url, request.method)

    resp = jsonify(msg)
    resp.status_code = 405
    return resp

def parse_arguments_to_user(form):
    email = str(request.form['email'])
    instrument = str(request.form['instrument'])

    if email == 'None':
        email = 'jhon@doe.com'
    if instrument == 'None':
        instrument = 'triangle'

    return User(email, instrument)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
