import unittest
import requests
import json
import random

class TestProfileNegative(unittest.TestCase):
    def test_add_user_positive(self):
        for _ in range(3):
            string = ''.join([chr(random.randint(65, 90)) for _ in range(9)])
            data = {
                'first_name': string,
                'second_name': string,
                'login': string,
                'password': string,
                'email': string,
            }
            print(data)
            resp = requests.post('http://127.0.0.1:5000/register', json=data)
            print(resp.text)
            response = json.loads(resp.text)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(response['status'], 1)
            print('/register test_add_user: {}'.format(resp.text))

    def test_b_add_user(self):
        for _ in range(3):
            string = ''.join([chr(random.randint(58, 68)) for _ in range(9)])
            data = {
                'first_name': '{}'.format(string),
                'second_name': '{}'.format(string),
                'login': '{}'.format(string),
                'password': '{}'.format(string),
            }
            print(data)
            resp = requests.post('http://127.0.0.1:5000/register', json=data)
            print(resp.text)
            self.assertEqual(resp.status_code, 400)
            print('/register test_add_user: {}'.format(resp.text))

    def test_c_login_user(self):
        data = {
            'login': '',
            'password': '',
        }
        resp = requests.post('http://127.0.0.1:5000/login', json=data)
        self.assertEqual(resp.status_code, 400)
        print('/login login_user: {}'.format(resp.text))

    def test_d_update_user(self):
        string = ''.join([chr(random.randint(65, 90)) for _ in range(9)])
        resp = requests.get('http://127.0.0.1:5000/profile/all')
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.text)
        users = json.loads(resp.text)
        for user in users:
            if user['id'] != 325:
                # Неизвестное поле. Менять можно только fist_name/second_name
                data = {
                    string: string,
                    string: string,
                }
                resp = requests.put('http://127.0.0.1:5000/profile/{}'.format(user['id']), json=data)
                self.assertEqual(resp.status_code, 400)
                print('[1] /profile/{} update_user: {}'.format(user['id'], resp.text))

                # 1 эквивалентное поле не было изменено
                resp = requests.get('http://127.0.0.1:5000/profile/{}'.format(user['id']), json=data)
                response = json.loads(resp.text)
                data = {
                    'first_name': response['first_name'],
                    'second_name': string,
                }
                resp = requests.put('http://127.0.0.1:5000/profile/{}'.format(user['id']), json=data)
                response2 = json.loads(resp.text)
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(response2['status'], 1)
                self.assertIsNotNone(response2['message'])
                print('[2] /profile/{} update_user: {}'.format(user['id'], resp.text))

    # POSITIVE
    def test_e_del_user_positive(self):
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

if __name__ == '__main__':
    unittest.main()
