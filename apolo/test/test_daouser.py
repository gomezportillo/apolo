# Source https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html#basic-definition
# This allows us to perform relative imports
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import unittest
from model.daouser import DAOUser
from model.user import User


MONGODB_URI = 'mongodb://user:user123@ds024548.mlab.com:24548/apolo-mongodb'
COLLECTION_NAME = 'test'

class TestDAO(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.daouser = DAOUser(MONGODB_URI)
        self.daouser.deleteAll()

    @classmethod
    def tearDownClass(self):
        self.daouser.deleteAll()

    def test_empty(self):
        self.daouser.deleteAll()

        users = self.daouser.readAll()
        self.assertEqual(len(users), 0)

    def test_insert(self):
        self.daouser.deleteAll()

        u = User("insert@user", "guitar")
        self.daouser.insert(u)
        result = self.daouser.readAll()
        self.assertEqual(1, len(result))

    def test_delete(self):
        self.daouser.deleteAll()

        u = User("delete@user", "guitar")
        self.daouser.insert(u)
        resp = self.daouser.delete(u)
        result = self.daouser.readAll()
        self.assertEqual(0, len(result))

    def test_find(self):
        self.daouser.deleteAll()

        u = User("find@user", "guitar")
        self.daouser.insert(u)
        result = self.daouser.find(u)
        self.assertEqual(u.toDict(), result)

    def test_update(self):
        self.daouser.deleteAll()

        u1 = User("update@user", "guitar")
        self.daouser.insert(u1)
        u1.instrument = "bass"
        self.daouser.update(u1)

        u2 = User(u1.email, "")
        result = self.daouser.find(u2)

        self.assertEqual(u1.toDict(), result)

if __name__ == '__main__':
    unittest.main()
