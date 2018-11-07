import os
from flask import Flask
from flask import request
import json
import pymongo

app = Flask(__name__)
MONGODB_URI = 'mongodb://user:user123@ds024548.mlab.com:24548/apolo-mongodb'
mongo_client = pymongo.MongoClient(MONGODB_URI)
apolo_ddbb = mongo_client.get_default_database() # as im using a sadxbox mlab account

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

@app.route('/add')
def add():
    email = str(request.args.get('email'))
    instrument = str(request.args.get('instrument'))

    if email == 'None':
        email = 'jhon@doe.com'
    if instrument == 'None':
        instrument = 'triangle'

    new_user = {}
    new_user['email'] = email
    new_user['instrument'] = instrument

    users_collection = apolo_ddbb['users']
    users_collection.insert(new_user)

    result = {}
    result['status'] = 'OK'
    result['message'] = 'User with email {} added successfully'.format(email)
    return json.dumps(result)

@app.route('/readall')
def readall():
    users_collection = apolo_ddbb['users']
    cursor = users_collection.find()

    users = {}
    for doc in cursor:
        try:
            users[ doc['email'] ] = doc['instrument']
        except KeyError:
            pass

    return json.dumps(users)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
