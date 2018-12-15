import pymongo

from model import user

PRIMARY_KEY = 'email'
COLLECTION_NAME = 'users'

class DAOUser:

    def __init__(self, MONGODB_URI):
        self.mongo_client = pymongo.MongoClient(MONGODB_URI)
        self.apolo_ddbb = self.mongo_client.get_database() # default ddbb as im using a sadxbox mlab account
        self.collection = self.apolo_ddbb[COLLECTION_NAME]

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

    def delete(self, user):
        criteria = {'email' : user.email}

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

    def find(self, user):
        criteria = {}
        if user.email != '':
            criteria['email'] = user.email
        if user.instrument != '':
            criteria['instrument'] = user.instrument

        cursor = self.collection.find( criteria )

        found_users = {}
        for doc in cursor:
            try:
                found_users['email'] = doc['email']
                found_users['instrument'] = doc['instrument']
            except KeyError:
                pass

        return found_users


    def set_up_ddbb(self):
        # setting up a primary key, or index in mongodb
        self.collection.create_index([(PRIMARY_KEY, pymongo.ASCENDING)], unique=True)
