import unittest
import requests


class Test(unittest.TestCase):

    def get_user(self):
        for ID in range(10):
            resp = requests.get('http://127.0.0.1/profile/{}'.format(ID))
            self.assertEqual(resp.status_code, 200)
            self.assertIsNotNone(resp.text)

    def get_users(self):
        resp = requests.get('http://127.0.0.1/profiles')
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.text)

    def login_user(self):
        data = {
            'login': 'SergeyAstapov',
            'password': 'SergeyAstapov123',
        }
        resp = requests.post('http://127.0.0.1/login', json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.text)

    def test_add_user(self):
        data = {
            'first_name': 'Sergey',
            'second_name': 'Astapov',
            'login': 'SergeyAstapov',
            'password': 'SergeyAstapov123',
            'confirm_password': 'SergeyAstapov123',
        }
        resp = requests.post('http://127.0.0.1/register', json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.text)

