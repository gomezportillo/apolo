from aux import *

from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import json


# App definition
app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/about', methods=['GET'])
def about():
    server_info['ruta'] = request.url
    return Response(json.dumps(server_info), status=200, mimetype='application/json')


@app.route('/log', methods=['GET'])
def log():
    file = open(LOG_FILE, 'r')
    return Response(file.read(), status=200, mimetype='application/json')


@app.route('/users', methods=['PUT'])
def insert():
    new_user = parse_arguments_to_user( request.form )
    status = daouser.insert( new_user )

    result = {}
    result['status'] = status
    result['message'] = 'On adding user with email {} '.format(new_user.email)

    app.logger.info( result )

    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route('/users', methods=['POST'])
def update():
    user = parse_arguments_to_user( request.form )
    status = daouser.update(user)

    result = {}
    result['status'] = status
    result['message'] = 'On updating user with email {} '.format(user.email)

    app.logger.info( result )

    return Response(json.dumps(result), status=200, mimetype='application/json')



@app.route('/users', methods=['DELETE'])
def delete():
    user = parse_arguments_to_user( request.form )
    status = daouser.delete(user)

    result = {}
    result['status'] = status
    result['message'] = 'On deleting user with email {} '.format(user.email)

    app.logger.info( result )

    return Response(json.dumps(result), status=200, mimetype='application/json')


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

    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route('/users/all', methods=['GET'])
def readall():
    users = daouser.readAll()
    return Response(json.dumps(users), status=200, mimetype='application/json')


@app.route('/users/all', methods=['DELETE'])
def deleteAll():
    status = daouser.deleteAll()

    result = {}
    result['status'] = status
    result['message'] = 'On deleting all users'

    app.logger.info( result )

    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.errorhandler(404)
def not_found(error=None):
    msg = {}
    msg['status'] = 404
    msg['message'] = 'URL {} not found'.format(request.url)

    app.logger.info( msg )

    return Response(json.dumps(msg), status=404, mimetype='application/json')


@app.errorhandler(405)
def not_allowed(error=None):
    msg = {}
    msg['status'] = 405
    msg['message'] = 'URL {} not allowed from {} HTTP method'.format(request.url, request.method)

    app.logger.info( msg )

    return Response(json.dumps(msg), status=405, mimetype='application/json')


def parse_arguments_to_user(form):
    email = str(request.form['email'])
    instrument = str(request.form['instrument'])

    if email == 'None':
        email = 'jhon@doe.com'
    if instrument == 'None':
        instrument = 'triangle'

    return User(email, instrument)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)
