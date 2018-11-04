import os
from flask import Flask
from flask import request
import json
import pymongo

app = Flask(__name__)

@app.route('/')
def index():
    data = {}
    data['status'] = 'OK'
    data['ruta'] = request.url
    json_data = json.dumps(data)
    return json_data

@app.route('/about')
def about():
    data = {}
    data['status'] = 'OK'
    data['author'] = 'Pedro Manuel Gomez-Portillo López'
    return json.dumps(data)

@app.route('/upper')
def toUpper():
    word = request.args.get('word')
    data = {}
    data['status'] = 'OK'
    data['word'] = str(word).upper()
    return json.dumps(data)

@app.route('/lower')
def toLower():
    word = request.args.get('word')
    data = {}
    data['status'] = 'OK'
    data['word'] = str(word).lower()
    return json.dumps(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
