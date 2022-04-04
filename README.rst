django-formapi
==============

Create JSON API:s with HMAC authentication and Django form-validation.

.. image:: https://travis-ci.com/5monkeys/django-formapi.svg?branch=master
    :target: http://travis-ci.com/5monkeys/django-formapi
.. image:: https://coveralls.io/repos/github/5monkeys/django-formapi/badge.svg?branch=master
    :target: https://coveralls.io/github/5monkeys/django-formapi?branch=master
.. image:: https://badge.fury.io/py/django-formapi.svg
    :target: https://badge.fury.io/py/django-formapi
.. image:: https://img.shields.io/pypi/l/django-formapi.svg
    :target: https://pypi.python.org/pypi/django-formapi
.. image:: https://img.shields.io/pypi/wheel/django-formapi.svg
    :target: https://pypi.python.org/pypi/django-formapi
.. image:: https://img.shields.io/pypi/pyversions/django-formapi.svg
    :target: https://pypi.python.org/pypi/django-formapi
.. image:: https://img.shields.io/pypi/dm/django-formapi.svg
    :target: https://pypi.python.org/pypi/django-formapi


Version compatibility
---------------------

See Travis-CI page for actual test results:
https://travis-ci.com/5monkeys/django-formapi

======  ===
Django  3.6
======  ===
 3.2    Yes
======  ===


Installation
------------

Install django-formapi in your python environment

.. code:: sh

    $ pip install django-formapi

Add ``formapi`` to your ``INSTALLED_APPS`` setting.

.. code:: python

    INSTALLED_APPS = (
        ...,
        "formapi",
    )

Add ``formapi.urls`` to your urls.py.

.. code:: python

  urlpatterns = patterns(
      ...,
      url(r"^api/", include("formapi.urls")),
  )

Usage
-----

Go ahead and create a ``calls.py``.

.. code:: python

  class DivisionCall(calls.APICall):
      """
      Returns the quotient of two integers
      """

      dividend = forms.FloatField()
      divisor = forms.FloatField()

      def action(self, test):
          dividend = self.cleaned_data.get("dividend")
          divisor = self.cleaned_data.get("divisor")
          return dividend / divisor


  API.register(DivisionCall, "math", "divide", version="v1.0.0")


Just create a class like your regular Django Forms but inheriting from ``APICall``. Define the fields that your API-call
should receive. The ``action`` method is called when your fields have been validated and what is returned will be JSON-encoded
as a response to the API-caller. The ``API.register`` call takes your ``APICall``-class as first argument, the second argument is
the ``namespace`` the API-call should reside in, the third argument is the ``name`` of your call and the fourth the ``version``.
This will result in an url in the form of ``api/[version]/[namespace]/[call_name]/`` so we would get ``/api/v1.0.0/math/divide/``.

A valid call with the parameters ``{'dividend': 5, 'divisor': 2}`` would result in this response:

.. code:: javascript

  {"errors": {}, "data": 5, "success": true}

An invalid call with the parameters ``{'dividend': "five", 'divisor': 2}`` would result in this response:

.. code:: javascript

  {"errors": {"dividend": ["Enter a number."]}, "data": false, "success": false}


Authentication
--------------
By default ``APICalls`` have HMAC-authentication turned on. Disable it by setting ``signed_requests = False`` on your ``APICall``.

If not disabled users of the API will have to sign their calls. To do this they need a ``secret`` generate, create a ``APIKey`` through the django
admin interface. On save a personal ``secret`` and ``key`` will be generated for the API-user.

To build a call signature for the ``DivisonCall`` create a querystring of the calls parameters sorted by the keys ``dividend=5&divisor=2``. Create a HMAC using SHA1 hash function.
Example in python:

.. code:: python

  import hmac
  from hashlib import sha1

  hmac_sign = hmac.new(secret, urllib2.quote("dividend=5&divisor=2"), sha1).hexdigest()

A signed request against ``DivisionCall`` would have the parameters ``{'dividend': 5, 'divisor': 2, 'key': generated_key, 'sign': hmac_sign}``

Documentation
-------------
Visit ``/api/discover`` for a brief documentation of the registered API-calls.
