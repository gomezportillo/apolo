import os
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello JJ!'

@app.route('/upper')
def toUpper():
    word = request.args.get('word')
    return str(word).upper()

@app.route('/lower')
def toLower():
    word = request.args.get('word')
    return str(word).lower()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
