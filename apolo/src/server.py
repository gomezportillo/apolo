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
    user = str(request.args.get('user'))
    instrument = str(request.args.get('instrument'))

    if user == 'None':
        user = 'jhon doe'
    if instrument == 'None':
        instrument = 'triangle'

    new_user = {}
    new_user['user'] = user
    new_user['instrument'] = instrument

    users_collection = apolo_ddbb['users']
    users_collection.insert(new_user)

    result = {}
    result['status'] = 'OK'
    result['message'] = 'User {} added successfully'.format(user)
    return json.dumps(result)

@app.route('/readall')
def readall():
    apolo_ddbb = mongo_client['apolo']
    result = apolo_ddbb['users'].find()
    print ("=========================================")
    for doc in result:
        print (doc)
    print ("=========================================")
    return json.dumps(result)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
