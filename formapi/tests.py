import json
from datetime import date, datetime, time
from decimal import Decimal
from functools import partial

import pytz
from django.contrib.auth import get_user_model
from django.forms import IntegerField
from django.test import Client, TransactionTestCase
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy

from formapi.api import DjangoJSONEncoder
from formapi.models import APIKey
from formapi.utils import get_sign, prepare_uuid_string

TOTAL_TESTS = 19


class SignedRequestTest(TransactionTestCase):
    def setUp(self):
        self.api_key = APIKey.objects.create(email="test@example.com")
        self.api_key_revoked = APIKey.objects.create(
            email="test3@example.com", revoked=True
        )
        self.client = Client()
        self.user = get_user_model().objects.create(
            email="user@example.com", username="räksmörgås"
        )
        self.user.set_password("rosebud")
        self.user.save()
        self.authenticate_url = "/api/v1.0.0/user/authenticate/"
        self.language_url = "/api/v1.0.0/comp/lang/"

    def send_request(self, url, data, key=None, secret=None, req_method="POST"):
        if not key:
            key = self.api_key.key
        if not secret:
            secret = self.api_key.secret
        sign = get_sign(secret, **data)
        data["key"] = key
        data["sign"] = sign
        if req_method == "POST":
            return self.client.post(url, data)
        elif req_method == "GET":
            return self.client.get(url, data)

    def test_api_key(self):
        smart_str(self.api_key)

    def test_api_key_gets_prepared_uuid_str_on_assignment(self):
        # Intentionally get key again
        test_key = APIKey.objects.get(email="test@example.com")

        self.assertEqual(test_key.key, prepare_uuid_string(test_key.key))

    def test_valid_auth(self):
        response = self.send_request(
            self.authenticate_url,
            {"username": self.user.username, "password": "rosebud"},
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(smart_str(response.content))
        self.assertEqual(response_data["errors"], {})
        self.assertTrue(response_data["success"])
        self.assertIsNotNone(response_data["data"])

    def test_invalid_call(self):
        response = self.send_request(
            "/api/v1.0.0/math/subtract/",
            {"username": self.user.username, "password": "rosebud"},
        )
        self.assertEqual(response.status_code, 404)

    def test_unsigned_auth(self):
        data = {"username": self.user.username, "password": "rosebud"}
        response = self.client.post(self.authenticate_url, data)
        self.assertEqual(response.status_code, 401)

    def test_invalid_sign(self):
        data = {"username": self.user.username, "password": "rosebud"}
        sign = get_sign(self.api_key.secret, **data)
        data["key"] = self.api_key.key
        data["sign"] = sign + "bug"
        response = self.client.post(self.authenticate_url, data)
        self.assertEqual(response.status_code, 401)

    def test_invalid_password(self):
        data = {"username": self.user.username, "password": "1337hax/x"}
        response = self.send_request(self.authenticate_url, data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(smart_str(response.content))
        self.assertGreater(len(response_data["errors"]), 0)
        self.assertFalse(response_data["success"])
        self.assertFalse(response_data["data"])

    def test_invalid_parameters(self):
        data = {"email": self.user.email, "password": "rosebud"}
        response = self.send_request(self.authenticate_url, data)
        self.assertEqual(response.status_code, 401)

    def test_revoked_api_key(self):
        data = {"username": self.user.username, "password": "rosebud"}
        response = self.send_request(
            self.authenticate_url,
            data,
            self.api_key_revoked.key,
            self.api_key_revoked.secret,
        )
        self.assertEqual(response.status_code, 401)

    def test_get_call(self):
        data = {"username": self.user.username, "password": "1337haxx"}
        response = self.send_request(self.authenticate_url, data, req_method="GET")
        self.assertEqual(response.status_code, 200)

    def test_multiple_values(self):
        data = {"languages": ["python", "java"]}
        response = self.send_request(self.language_url, data, req_method="GET")
        self.assertEqual(response.status_code, 200)


class HMACTest(TransactionTestCase):
    def setUp(self):
        self.api_key = APIKey.objects.create(email="test@example.com")

    def test_parameter_sign(self):
        # test unicode
        url_params = "first_name=mårten&last_name=superkebab"
        dict_params = {"first_name": "mårten", "last_name": "superkebab"}
        self.assert_equal_signs(url_params, dict_params)
        # test string
        url_params = "first_name=mårten&last_name=superkebab"
        dict_params = {"first_name": "mårten", "last_name": "superkebab"}
        self.assert_equal_signs(url_params, dict_params)
        # test integer
        url_params = "dividend=4&divisor=2"
        dict_params = {"dividend": 4, "divisor": 2}
        self.assert_equal_signs(url_params, dict_params)
        # test boolean
        url_params = "secure=True"
        dict_params = {"secure": True}
        self.assert_equal_signs(url_params, dict_params)

    def assert_equal_signs(self, url_params, dict_params):
        sign1 = get_sign(self.api_key.secret, querystring=url_params)
        sign2 = get_sign(self.api_key.secret, **dict_params)
        self.assertEqual(sign1, sign2)


class UnsignedRequestTest(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.divide_url = "/api/v1.0.0/math/divide/"

    def test_ok_call(self):
        data = {"dividend": 7, "divisor": 2}
        response = self.client.post(self.divide_url, data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(smart_str(response.content))
        self.assertEqual(response_data["data"], 3.5)

    def test_invalid_call(self):
        data = {"dividend": "a", "divisor": 2}
        response = self.client.post(self.divide_url, data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(smart_str(response.content))
        dividend_error = response_data["errors"]["dividend"]
        self.assertEqual(
            dividend_error[0], smart_str(IntegerField().error_messages["invalid"])
        )
        self.assertGreater(len(response_data["errors"]), 0)
        self.assertFalse(response_data["success"])
        self.assertFalse(response_data["data"])

    def test_error_call(self):
        data = {"dividend": "42", "divisor": 0}
        response = self.client.post(self.divide_url, data)
        response_data = json.loads(smart_str(response.content))
        self.assertFalse(response_data["success"])


class JSONEncoderTest(TransactionTestCase):
    def setUp(self):
        self.dumps = partial(json.dumps, cls=DjangoJSONEncoder)

    def test_datetime_encode(self):
        naive_micro_datetime = {"datetime": datetime.now(), "int": 1}
        self.dumps(naive_micro_datetime)

        naive_second_datetime = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.dumps(naive_second_datetime)

        tz_utc_datetime = {"datetime": datetime.now().replace(tzinfo=pytz.UTC)}
        self.dumps(tz_utc_datetime)

        datetime_date = {"datetime": date.today()}
        self.dumps(datetime_date)

        naive_datetime_time = {"datetime": time()}
        self.dumps(naive_datetime_time)

        naive_datetime_micro_time = {"datetime": time(microsecond=100)}
        self.dumps(naive_datetime_micro_time)

    def test_decimal_encode(self):
        decimal_data = {"decimal": Decimal("1.504")}
        self.dumps(decimal_data)

    def test_queryset(self):
        user_manager = get_user_model().objects
        user_manager.create(username="test", email="test@example.com")
        queryset = {"queryset": user_manager.all()}
        self.dumps(queryset)
        self.dumps(user_manager.all())

    def test_gettext(self):
        gettext_data = {"gettext": ugettext_lazy("tränslate me please")}
        self.dumps(gettext_data)
