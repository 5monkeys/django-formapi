# coding=utf-8
import json
from django.contrib.auth.models import User
from django.test import TransactionTestCase, Client
from formapi.models import APIKey
from formapi.utils import get_sign


class SignedAuthRequestTest(TransactionTestCase):

    def setUp(self):
        self.api_key = APIKey.objects.create(email="test@example.com")
        self.client = Client()
        self.user = User.objects.create(email="user@example.com", username="räksmörgås")
        self.user.set_password("rosebud")
        self.user.save()
        self.authenticate_url = '/api/v1.0.0/user/authenticate/'

    def send_request(self, url, data, key=None, secret=None):
        if not key:
            key = self.api_key.key
        if not secret:
            secret = self.api_key.secret
        sign = get_sign(secret, **data)
        data['key'] = key
        data['sign'] = sign
        return self.client.post(url, data)

    def test_valid_auth(self):
        data = {'username': self.user.username, 'password': 'rosebud'}
        response = self.send_request(self.authenticate_url, data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['errors'], {})
        self.assertTrue(response_data['success'])
        self.assertIsNotNone(response_data['data'])

    def test_unsigned_auth(self):
        data = {'username': self.user.username, 'password': 'rosebud'}
        response = self.client.post(self.authenticate_url, data)
        self.assertEqual(response.status_code, 401)

    def test_invalid_password(self):
        data = {'username': self.user.username, 'password': '1337haxx'}
        response = self.send_request(self.authenticate_url, data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertGreater(len(response_data['errors']), 0)
        self.assertFalse(response_data['success'])
        self.assertFalse(response_data['data'])

    def test_invalid_parameters(self):
        data = {'email': self.user.email, 'password': 'rosebud'}
        response = self.send_request(self.authenticate_url, data)
        self.assertEqual(response.status_code, 401)

