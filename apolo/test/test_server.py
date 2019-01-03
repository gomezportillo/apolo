import unittest
import requests
import json

class TestServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.port = 80
        self.URL_BASE      = 'http://localhost:{}'.format( self.port )
        self.URL_USERS     = self.URL_BASE + '/rest/users'
        self.URL_USERS_ALL = self.URL_USERS + '/all'

        requests.delete( self.URL_USERS_ALL )


    @classmethod
    def tearDownClass(self):
        requests.delete( self.URL_USERS_ALL )


    def test_index_is_up(self):
        response = requests.get( self.URL_BASE )
        self.assertEqual(response.status_code, 200)


    def test_index_message(self):
        response = requests.get( self.URL_BASE )
        response_json = response.json()
        self.assertEqual(response_json['status'], 'OK')


    def test_insert_is_up(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.put( self.URL_USERS, data=user )
        self.assertEqual( response.status_code, 200 )

        requests.delete( self.URL_USERS_ALL )


    def test_insert(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.put( self.URL_USERS, data=user)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'SUCCESS')

        requests.delete( self.URL_USERS_ALL )


    def test_find_is_up(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.get( self.URL_USERS, data=user )
        self.assertEqual( response.status_code, 200 )

        requests.delete( self.URL_USERS_ALL )


    def test_find_user(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        requests.put( self.URL_USERS, data=user )
        response = requests.get( self.URL_USERS, data=user )
        response_json = response.json()
        response_json['message']
        self.assertEqual( [user], response_json['message'] )

        requests.delete( self.URL_USERS_ALL )


    def test_update_is_up(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.post( self.URL_USERS, data=user )
        self.assertEqual(response.status_code, 200)

        requests.delete( self.URL_USERS_ALL )


    def test_update_user(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        requests.put(self.URL_USERS, data=user)
        user['instrument'] = 'bass'
        requests.post(self.URL_USERS, data=user)
        response = requests.get(self.URL_USERS, data=user)
        response_json = response.json()
        self.assertEqual( [user], response_json['message'] )

        requests.delete( self.URL_USERS_ALL )


    def test_delete_is_up(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.delete( self.URL_USERS, data=user )
        self.assertEqual( response.status_code, 200 )


    def test_delete_user(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        requests.put( self.URL_USERS, data=user )
        response = requests.delete( self.URL_USERS, data=user )
        response = requests.get( self.URL_USERS, data=user )
        response_json = response.json()
        self.assertEqual( [], response_json['message'] )

        requests.delete( self.URL_USERS_ALL )


    def test_readall_is_up(self):
        response = requests.get( self.URL_USERS_ALL )
        self.assertEqual( response.status_code, 200 )


if __name__ == '__main__':
    unittest.main()
