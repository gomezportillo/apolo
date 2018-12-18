# The aim of this file is to clarify the server code

import os
import logging
import pymongo
import logging
import datetime
import shutil

from model.user import User
from model.daouser import DAOUser

# Metadata
VERSION = '5.0'

server_info = {}
server_info['version']      = VERSION
server_info['status_code']  = 200
server_info['status']       = 'OK'
server_info['author']       = 'Pedro Manuel Gomez-Portillo Lopez'
server_info['project']      = 'Apolo'


# Log configuration
if os.path.exists('logs'):
    shutil.rmtree('logs')
os.makedirs('logs')

LOG_FILE = os.path.join('logs', 'apolo.log')

f = open(LOG_FILE, 'w')
f.write( "Welcome to the Apolo log file! <3\n" )
f.write( "Server started on {}\n".format( datetime.datetime.now() ))
f.close()

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)


# MongoDB configuration
MONGODB_URI = 'mongodb://user:user123@ds024548.mlab.com:24548/apolo-mongodb'


# DAO user
daouser = DAOUser( MONGODB_URI )
