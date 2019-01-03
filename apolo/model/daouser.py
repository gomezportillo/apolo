# Source https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html#basic-definition
# This allows to perform relative imports
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import pymongo

from model import user
from auxiliary.singleton import Singleton

MONGODB_URI      = 'mongodb://user:user123@ds024548.mlab.com:24548/apolo-mongodb'
PRIMARY_KEY      = 'email'
COLLECTION_USERS = 'users'


@Singleton
class DAOUser:

    def __init__(self):
        self.mongo_client = pymongo.MongoClient( MONGODB_URI )
        self.apolo_ddbb   = self.mongo_client.get_database() # default ddbb as im using a sadxbox mlab account
        self.collection   = self.apolo_ddbb[ COLLECTION_USERS ]

        self.set_up_ddbb()


    def insert(self, user):
        try:
            result = self.collection.insert_one(user.toDict())
        except pymongo.errors.DuplicateKeyError:
            return 'EMAIL_ALREADY_EXISTS'
        except:
            return 'ERROR'
        return 'SUCCESS'


    def update(self, user):
        criteria = {'email' : user.email}
        changes = {'$set': {'instrument' : user.instrument}}

        try:
            result = self.collection.update_one(criteria, changes)
            if result['updatedExisting']:
                return 'SUCCESS'
            else:
                return 'EMAIL_NOT_EXISTING'
        except:
            return 'ERROR'


    def readAll(self):
        cursor = self.collection.find()

        users = {}
        for doc in cursor:
            try:
                users[ doc['email'] ] = doc['instrument']
            except KeyError:
                pass

        return users


    def delete(self, email):
        criteria = {'email' : email}

        try:
            result = self.collection.delete_one(criteria)
        except:
            return 'ERROR'

        return 'SUCCESS'


    def deleteAll(self):
        try:
            self.collection.drop()
        except:
            return 'ERROR'

        return 'SUCCESS'


    def find(self, email):
        criteria = {'email' : email}

        cursor = self.collection.find( criteria )

        found_users = []
        for doc in cursor:
            try:
                user = {'email': doc['email'], 'instrument': doc['instrument']}
                found_users.append( user )
            except KeyError:
                pass

        return found_users


    def set_up_ddbb(self):
        # setting up a primary key, or index in mongodb
        self.collection.create_index([(PRIMARY_KEY, pymongo.ASCENDING)], unique=True)
