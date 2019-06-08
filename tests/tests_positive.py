import unittest
import requests
import json
import random

class TestProfilePositive(unittest.TestCase):
    def test_add_user(self):
        for _ in range(3):
            string = ''.join([chr(random.randint(65, 90)) for _ in range(9)])
            data = {
                'first_name': string,
                'second_name': string,
                'login': string,
                'password': string,
            }
            print(data)
            resp = requests.post('http://127.0.0.1:5000/register', json=data)
            print(resp.text)
            response = json.loads(resp.text)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(response['status'], 1)
            print('/register test_add_user: {}'.format(resp.text))

    def test_c_login_user(self):
        resp = requests.get('http://127.0.0.1:5000/profile/all')
        print(resp.status_code)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.text)
        users = json.loads(resp.text)
        for user in users:
            if user['id'] != 325:
                data = {
                    'login': user['first_name'],
                    'password': user['first_name'],
                }
                print(data)
                resp = requests.post('http://127.0.0.1:5000/login', json=data)
                print('/login login_user: {}'.format(resp.text))
                print(resp.status_code)
                self.assertEqual(resp.status_code, 200)
                self.assertGreater(user['id'], 0)
                self.assertIsNotNone(resp.text)

    def test_d_update_user(self):
        string = ''.join([chr(random.randint(65, 90)) for _ in range(9)])
        resp = requests.get('http://127.0.0.1:5000/profile/all')
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.text)
        users = json.loads(resp.text)
        for user in users:
            if user['id'] != 325:
                # Неизвестное поле. Менять можно только fist_name/second_name
                # {'status': 1}
                data = {
                    'first_name': string ,
                    'second_name': string + 'a',
                }
                resp = requests.put('http://127.0.0.1:5000/profile/{}'.format(user['id']), json=data)
                response = json.loads(resp.text)
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(response['status'], 1)
                print('[3] /profile/{} update_user: {}'.format(user['id'], resp.text))

    def test_e_del_user(self):
        resp = requests.get('http://127.0.0.1:5000/profile/all')
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.text)
        users = json.loads(resp.text)
        for user in users:
            if user['id'] != 325:
                resp = requests.delete('http://127.0.0.1:5000/profile/{}'.format(user['id']))
                response = json.loads(resp.text)
                self.assertEqual(resp.status_code, 200)
                self.assertIsNotNone(resp.text)
                self.assertEqual(response['status'], 1)
                print('/profile/{} del_user: {}'.format(user['id'], resp.text))