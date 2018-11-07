import pymongo

from model import user

class DAOUser:

    def __init__(self, MONGODB_URI, COLLECTION_NAME):
        self.mongo_client = pymongo.MongoClient(MONGODB_URI)
        self.apolo_ddbb = self.mongo_client.get_default_database() # as im using a sadxbox mlab account
        self.collection = self.apolo_ddbb[COLLECTION_NAME]

    def insert(self, user):
        try:
            self.collection.insert(user.toDict())
        except:
            return 'ERROR'

        return 'SUCCESS'

    def update(self, user):
        criteria = {'email' : user.email}
        changes = {'$set': {'instrument' : user.instrument}}

        try:
            self.collection.update(criteria, changes)
        except:
            return 'ERROR'

        return 'SUCCESS'

    def readAll(self):
        cursor = self.collection.find()

        users = {}
        for doc in cursor:
            try:
                users[ doc['email'] ] = doc['instrument']
            except KeyError:
                pass
        
        return users
