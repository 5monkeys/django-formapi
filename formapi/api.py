from collections import defaultdict
from decimal import Decimal
import decimal
import hmac
import logging
import urllib2
from hashlib import sha1
from json import dumps, loads, JSONEncoder
import datetime
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator, classonlymethod
from django.utils.encoding import force_unicode
from django.utils.importlib import import_module
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.db.models.query import QuerySet, ValuesQuerySet
from django.utils.functional import curry, Promise
from .models import APIKey

LOG = logging.getLogger('formapi')


def autodiscover():
    for app in settings.INSTALLED_APPS:
        try:
            import_module('%s.calls' % app)
        except ImportError:
            continue


class AddHeaderAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        msg = ' '.join((self.extra.get('header'), msg))
        return msg, kwargs


class DjangoJSONEncoder(JSONEncoder):

    def default(self, obj):
        date_obj = self.default_date(obj)
        if date_obj:
            return date_obj
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, Decimal):
            return "%.2f" % obj
        if isinstance(obj, ValuesQuerySet):
            return list(obj)
        elif isinstance(obj, QuerySet):
            return loads(serializers.serialize('json', obj))
        elif isinstance(obj, Promise):
            return force_unicode(obj)

        return JSONEncoder.default(self, obj)

    def default_date(self, obj):
        if isinstance(obj, datetime.datetime):
            r = obj.isoformat()
            if obj.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            if obj.tzinfo is not None and obj.tzinfo.utcoffset(obj) is not None:
                raise ValueError("JSON can't represent timezone-aware times.")
            r = obj.isoformat()
            if obj.microsecond:
                r = r[:12]
            return r

dumps = curry(dumps, cls=DjangoJSONEncoder)


class API(FormView):
    template_name = 'formapi/api/form.html'
    signed_requests = True
    call_mapping = defaultdict(lambda: defaultdict(dict))

    @classmethod
    def register(cls, call_cls, namespace, name=None, version='beta'):
        call_name = name or call_cls.__name__
        API.call_mapping[version][namespace][call_name] = call_cls

    @classonlymethod
    def as_view(cls, **initkwargs):
        autodiscover()
        return super(API, cls).as_view(**initkwargs)

    def get_form_class(self):
        try:
            return API.call_mapping[self.version][self.namespace][self.call]
        except KeyError:
            raise Http404

    def get_access_params(self):
        key = self.request.REQUEST.get('key')
        sign = self.request.REQUEST.get('sign')
        return key, sign

    def sign_ok(self, sign):
        validation_string = ''
        for field_name in sorted(self.get_form_class()().fields.keys()):
            param = self.request.REQUEST.get(field_name)
            if param is not None:
                validation_string += ''.join(('&', field_name, '=', param))
        validation_string = validation_string.lstrip('&')
        return sign == hmac.new(str(self.api_key.secret), urllib2.quote(validation_string.encode('utf-8')), sha1).hexdigest()

    def render_to_json_response(self, context, **response_kwargs):
        data = dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_valid(self, form):
        self.log.info('Valid form received')
        test_call = False
        if self.api_key:
            test_call = self.api_key.test
        data = form.action(test_call)
        response_data = {
            'success': not bool(len(form.errors)),
            'errors': form.errors,
            'data': data
        }
        return self.render_to_json_response(response_data)

    def form_invalid(self, form):
        self.log.info('Invalid form received')
        response_data = {
            'success': False,
            'errors': form.errors,
            'data': False
        }
        return self.render_to_json_response(response_data, status=400)

    def get_log_header(self):
        if not hasattr(self, 'log_header'):
            key = getattr(self, 'api_key', None)
            self.log_header = '[%s][%s][%s]' % (
                self.request.META['REMOTE_ADDR'],
                self.request.META['REQUEST_METHOD'],
                key.key if key else 'unknown')
        return self.log_header

    def setup_log(self, log):
        self.log = AddHeaderAdapter(log, {'header': self.get_log_header()})

    def authorize(self):
        if getattr(self.get_form_class(), 'signed_requests', API.signed_requests):
            key, sign = self.get_access_params()
            ### Check for not revoked api key
            try:
                self.api_key = APIKey.objects.get(key=key, revoked=False)
            except APIKey.DoesNotExist:
                return False
            ### Check request signature
            return self.sign_ok(sign)

        return True

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Set up request
        self.request = request

        # Set up form class
        self.version = kwargs['version']
        self.namespace = kwargs['namespace']
        self.call = kwargs['call']

        # Check access params
        self.api_key = None
        access_granted = self.authorize()
        # Setup logging to add header
        self.setup_log(LOG)

        # Authorize request
        if access_granted:
            self.log.info('Access Granted %s', self.request.REQUEST)
            return super(API, self).dispatch(request, *args, **kwargs)

        # Access denied
        self.log.info('Access Denied %s', self.request.REQUEST)

        return HttpResponse(status=401)
