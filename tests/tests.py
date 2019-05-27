import unittest
import requests


class TestUser(unittest.TestCase):

	def test_get_user(self)
		for ID in range(10):
			resp = requests.post('http://127.0.0.1/profile/{}'.format(ID), json=data)
			self.assertEqual(resp.status_code, 200)
			self.assertIsNotNone(resp.text)
		
		
	def test_get_users(self)
		resp = requests.post('http://127.0.0.1/profiles', json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.text)
		
		
	def test_login_user(self):
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

