# coding=utf-8
from datetime import datetime, date, time
from decimal import Decimal
import json
from django.contrib.auth.models import User
from django.forms import IntegerField
from django.test import TransactionTestCase, Client
from django.utils.functional import curry
from pytz import UTC
from django.utils.translation import ugettext_lazy
from formapi.api import DjangoJSONEncoder
from formapi.models import APIKey
from formapi.utils import get_sign


class SignedRequestTest(TransactionTestCase):

    def setUp(self):
        self.api_key = APIKey.objects.create(email="test@example.com")
        self.api_key_revoked = APIKey.objects.create(email="test3@example.com", revoked=True)
        self.client = Client()
        self.user = User.objects.create(email="user@example.com", username="räksmörgås")
        self.user.set_password("rosebud")
        self.user.save()
        self.authenticate_url = '/api/v1.0.0/user/authenticate/'

    def send_request(self, url, data, key=None, secret=None, req_method="POST"):
        if not key:
            key = self.api_key.key
        if not secret:
            secret = self.api_key.secret
        sign = get_sign(secret, **data)
        data['key'] = key
        data['sign'] = sign
        if req_method == 'POST':
            return self.client.post(url, data)
        elif req_method == 'GET':
            return self.client.get(url, data)

    def test_api_key(self):
        unicode(self.api_key)

    def test_valid_auth(self):
        response = self.send_request(self.authenticate_url, {'username': self.user.username, 'password': 'rosebud'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['errors'], {})
        self.assertTrue(response_data['success'])
        self.assertIsNotNone(response_data['data'])

    # def test_invalid_call(self):
    #     response = self.send_request('/api/v1.0.0/math/subtract/', {'username': self.user.username, 'password': 'rosebud'})
    #     self.assertEqual(response.status_code, 404)

    def test_unsigned_auth(self):
        data = {'username': self.user.username, 'password': 'rosebud'}
        response = self.client.post(self.authenticate_url, data)
        self.assertEqual(response.status_code, 401)

    def test_invalid_sign(self):
        data = {'username': self.user.username, 'password': 'rosebud'}
        sign = get_sign(self.api_key.secret, **data)
        data['key'] = self.api_key.key
        data['sign'] = sign + "bug"
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

    def test_revoked_api_key(self):
        data = {'username': self.user.username, 'password': 'rosebud'}
        response = self.send_request(self.authenticate_url, data, self.api_key_revoked.key, self.api_key_revoked.secret)
        self.assertEqual(response.status_code, 401)

    def test_get_call(self):
        data = {'username': self.user.username, 'password': '1337haxx'}
        response = self.send_request(self.authenticate_url, data, req_method='GET')
        self.assertEqual(response.status_code, 200)


class HMACTest(TransactionTestCase):

    def setUp(self):
        self.api_key = APIKey.objects.create(email="test@example.com")

    def test_paramater_sign(self):
        url_params = u'first_name=mårten&last_name=superkebab'
        dict_params = {'first_name': u'mårten', 'last_name': u'superkebab'}
        sign1 = get_sign(self.api_key.secret, querystring=url_params)
        sign2 = get_sign(self.api_key.secret, **dict_params)
        self.assertEqual(sign1, sign2)


class UnsignedRequestTest(TransactionTestCase):

    def setUp(self):
        self.client = Client()
        self.divide_url = '/api/v1.0.0/math/divide/'

    def test_ok_call(self):
        data = {'dividend': 7, 'divisor': 2}
        response = self.client.post(self.divide_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['data'], 3.5)

    def test_invalid_call(self):
        data = {'dividend': "a", 'divisor': 2}
        response = self.client.post(self.divide_url, data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        dividend_error = response_data['errors']['dividend']
        self.assertEqual(dividend_error[0], unicode(IntegerField().error_messages['invalid']))
        self.assertGreater(len(response_data['errors']), 0)
        self.assertFalse(response_data['success'])
        self.assertFalse(response_data['data'])

    def test_error_call(self):
        data = {'dividend': "42", 'divisor': 0}
        response = self.client.post(self.divide_url, data)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])


class JSONEncoderTest(TransactionTestCase):

    def setUp(self):
        self.dumps = curry(json.dumps, cls=DjangoJSONEncoder)

    def test_datetime_encode(self):
        naive_micro_datetime = {'datetime': datetime.now(), 'int': 1}
        self.dumps(naive_micro_datetime)

        naive_second_datetime = {'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.dumps(naive_second_datetime)

        tz_utc_datetime = {'datetime': datetime.now().replace(tzinfo=UTC)}
        self.dumps(tz_utc_datetime)

        datetime_date = {'datetime': date.today()}
        self.dumps(datetime_date)

        naive_datetime_time = {'datetime': time()}
        self.dumps(naive_datetime_time)

        naive_datetime_micro_time = {'datetime': time(microsecond=100)}
        self.dumps(naive_datetime_micro_time)

    def test_decimal_encode(self):
        decimal_data = {'decimal': Decimal("1.504")}
        self.dumps(decimal_data)

    def test_queryset(self):
        User.objects.create(username="test", email="test@example.com")
        queryset = {'queryset': User.objects.all()}
        self.dumps(queryset)
        self.dumps(User.objects.all())

    def test_values_list(self):
        User.objects.create(username="test", email="test@example.com")
        values = User.objects.values('id', 'email')
        self.dumps(values)
        values_list = User.objects.values_list('id', flat=True)
        self.dumps(values_list)

    def test_gettext(self):
        gettext_data = {'gettext': ugettext_lazy(u'tränslate me please')}
        self.dumps(gettext_data)
