import os
from flask import Flask
from flask import request
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
    return json.dumps(data)

@app.route('/about')
def about():
    data = {}
    data['status'] = 'OK'
    data['author'] = 'Pedro Manuel Gomez-Portillo López'
    return json.dumps(data)

@app.route('/insert')
def insert():
    new_user = parse_arguments_to_user( request.args )
    status = daouser.insert(new_user)

    result = {}
    result['status'] = status
    result['message'] = 'On adding user with email {} '.format(new_user.email)
    return json.dumps(result)

@app.route('/update')
def update():
    user = parse_arguments_to_user( request.args )
    status = daouser.update(user)

    result = {}
    result['status'] = status
    result['message'] = 'On updating user with email {} '.format(user.email)
    return json.dumps(result)

@app.route('/delete')
def delete():
    user = parse_arguments_to_user( request.args )
    status = daouser.delete(user)

    result = {}
    result['status'] = status
    result['message'] = 'On deleting user with email {} '.format(user.email)
    return json.dumps(result)

@app.route('/readall')
def readall():
    users = daouser.readAll()
    return json.dumps(users)

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
    return json.dumps(result)


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
