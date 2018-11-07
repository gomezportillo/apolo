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
def add():
    email = str(request.args.get('email'))
    instrument = str(request.args.get('instrument'))

    if email == 'None':
        email = 'jhon@doe.com'
    if instrument == 'None':
        instrument = 'triangle'

    new_user = User(email, instrument)
    status = daouser.insert(new_user)

    result = {}
    result['status'] = status
    result['message'] = 'On adding user with email {} '.format(email)
    return json.dumps(result)

@app.route('/readall')
def readall():
    users = daouser.readAll()
    return json.dumps(users)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
