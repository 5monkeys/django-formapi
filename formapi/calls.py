from django import forms
from django.core import serializers
from django.forms.forms import NON_FIELD_ERRORS
from django.shortcuts import get_object_or_404


class BaseAPICall(object):

    request_passed = False
    request_kwarg = 'request'

    def add_error(self, error_msg):
        errors = self.non_field_errors()
        errors.append(error_msg)
        self._errors[NON_FIELD_ERRORS] = errors

    def action(self, test):
        raise NotImplementedError('APIForms must implement action(self, test)')


class APICall(forms.Form, BaseAPICall):

    instance_kwargs = None


class APIModelCall(forms.ModelForm, BaseAPICall):

    instance_pk_param = '__instance_pk'
    pk_field = 'pk'

    @classmethod
    def get_instance(cls, request):
        instance_pk = request.REQUEST.get(cls.instance_pk_param, None)
        if instance_pk:
            model_class = cls._meta.model
            return get_object_or_404(model_class, **{cls.pk_field: cls.webiste_slug})
        return None

    def serialize_obj(self, obj):
        return serializers.serialize('json', [obj])[1:-1]

    def action(self, test):
        obj = self.save()
        return self.serialize_obj(obj)
