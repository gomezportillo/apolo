# Source https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html#basic-definition
# This allows to perform relative imports
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


import unittest
from apolo.model.daouser import DAOUser
from apolo.model.user import User


class TestDAO(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        DAOUser.instance().deleteAll()


    @classmethod
    def tearDownClass(self):
        DAOUser.instance().deleteAll()


    def test_empty(self):
        DAOUser.instance().deleteAll()

        users = DAOUser.instance().readAll()
        self.assertEqual( len(users), 0 )


    def test_insert(self):
        DAOUser.instance().deleteAll()

        u = User("insert@user", "guitar")
        DAOUser.instance().insert(u)
        result = DAOUser.instance().readAll()
        self.assertEqual( len(result), 1 )


    def test_delete(self):
        DAOUser.instance().deleteAll()

        u = User("delete@user", "guitar")
        DAOUser.instance().insert(u)
        resp = DAOUser.instance().delete( u.email )
        result = DAOUser.instance().readAll()
        self.assertEqual( len(result), 0 )


    def test_find(self):
        DAOUser.instance().deleteAll()

        u = User("find@user", "guitar")
        DAOUser.instance().insert(u)
        result = DAOUser.instance().find( u.email )
        self.assertEqual( [u.toDict()], result )


    def test_update(self):
        DAOUser.instance().deleteAll()

        u1 = User("update@user", "guitar")
        DAOUser.instance().insert( u1 )
        u1.instrument = "bass"
        DAOUser.instance().update( u1 )

        u2 = User(u1.email, "")
        result = DAOUser.instance().find( u2.email )

        self.assertEqual( [u1.toDict()] , result)


if __name__ == '__main__':
    unittest.main()
