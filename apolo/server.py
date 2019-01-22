from auxiliary.auxiliary import *

from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import json


# App definition
app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/about', methods=['GET'])
@app.route('/status', methods=['GET'])
def about():
    server_info['ruta'] = request.url
    return Response(json.dumps(server_info), status=200, mimetype='application/json')


@app.route('/log', methods=['GET'])
def log():
    file = open(LOG_FILE, 'r')
    return Response(file.read(), status=200, mimetype='text/plain')


@app.route('/rest/users', methods=['PUT'])
def insert():
    new_user = parse_arguments_to_user( request.form )
    status = DAOUser.instance().insert( new_user )

    result = {}
    result['status']  = status
    result['message'] = 'On adding user with email {} '.format(new_user.email)

    app.logger.info( result )

    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route('/rest/users', methods=['POST'])
def update():
    user = parse_arguments_to_user( request.form )
    status = DAOUser.instance().update(user)

    result = {}
    result['status']  = status
    result['message'] = 'On updating user with email {} '.format(user.email)

    app.logger.info( result )

    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route('/rest/users/<email>', methods=['DELETE'])
def delete(email):
    status = DAOUser.instance().delete( email )

    result = {}
    result['status']  = status
    result['message'] = 'On deleting user with email {} '.format( email )

    app.logger.info( result )

    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route('/rest/users/<email>',  methods=['GET'])
def find(email):
    users = DAOUser.instance().find( email )

    if not users:
        status = 'USER_NOT_FOUND'
    else:
        status = 'SUCCESS'

    result = {}
    result['status']  = status
    result['message'] = users

    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route('/rest/users/all', methods=['GET'])
def readall():
    users = DAOUser.instance().readAll()
    return Response(json.dumps(users), status=200, mimetype='application/json')


@app.route('/rest/users/all', methods=['DELETE'])
def deleteAll():
    status = DAOUser.instance().deleteAll()

    result = {}
    result['status']  = status
    result['message'] = 'On deleting all users'

    app.logger.info( result )

    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.errorhandler(404)
def not_found(error=None):
    message = {}
    message['status']  = 404
    message['message'] = 'URL {} not found'.format(request.url)

    app.logger.info( message )

    return Response(json.dumps(message), status=404, mimetype='application/json')


@app.errorhandler(405)
def not_allowed(error=None):
    message = {}
    message['status']  = 405
    message['message'] = 'URL {} not allowed from {} HTTP method'.format(request.url, request.method)

    app.logger.info( message )

    return Response(json.dumps(message), status=405, mimetype='application/json')


def parse_arguments_to_user(form):
    unparsed_email      = request.form['email']
    unparsed_instrument = request.form['instrument']

    email      = str(unparsed_email) if unparsed_email else 'jhon@doe.com'
    instrument = str(unparsed_instrument) if unparsed_instrument else 'triangle'

    return User(email, instrument)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)
