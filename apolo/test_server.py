import unittest
import requests
import json

class Test2(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        requests.delete('http://localhost:5000/deleteAll')

    @classmethod
    def tearDownClass(self):
        requests.delete('http://localhost:5000/deleteAll')

    def test_index_is_up(self):
        response = requests.get('http://localhost:5000/')
        self.assertEqual(response.status_code, 200)

    def test_index_message(self):
        response = requests.get('http://localhost:5000/')
        response_json = response.json()
        self.assertEqual(response_json['status'], 'OK')

    def test_insert_is_up(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.put('http://localhost:5000/users', data=user)
        self.assertEqual(response.status_code, 200)

        requests.delete('http://localhost:5000/deleteAll')

    def test_insert(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.put('http://localhost:5000/users', data=user)
        response_json = response.json()
        self.assertEqual(response_json['status'], 'SUCCESS')

        requests.delete('http://localhost:5000/deleteAll')

    def test_find_is_up(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.get('http://localhost:5000/users', data=user)
        self.assertEqual(response.status_code, 200)

        requests.delete('http://localhost:5000/deleteAll')

    def test_find_user(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        requests.put('http://localhost:5000/users', data=user)
        response = requests.get('http://localhost:5000/users', data=user)
        response_json = response.json()
        response_json['message']
        self.assertEqual(user, response_json['message'])

        requests.delete('http://localhost:5000/deleteAll')

    def test_update_is_up(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.post('http://localhost:5000/users', data=user)
        self.assertEqual(response.status_code, 200)

        requests.delete('http://localhost:5000/deleteAll')

    def test_update_user(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        requests.put('http://localhost:5000/users', data=user)
        user['instrument'] = 'bass'
        requests.post('http://localhost:5000/users', data=user)
        response = requests.get('http://localhost:5000/users', data=user)
        response_json = response.json()
        self.assertEqual(user, response_json['message'])

        requests.delete('http://localhost:5000/deleteAll')

    def test_delete_is_up(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        response = requests.delete('http://localhost:5000/users', data=user)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        user={'email':'jhon@doe', 'instrument': 'guitar'}
        requests.put('http://localhost:5000/users', data=user)
        response = requests.delete('http://localhost:5000/users', data=user)
        response = requests.get('http://localhost:5000/users', data=user)
        response_json = response.json()
        self.assertEqual({}, response_json['message'])

        requests.delete('http://localhost:5000/deleteAll')


if __name__ == '__main__':
    unittest.main()
