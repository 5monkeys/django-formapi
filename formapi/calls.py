# coding=utf-8
import django
from django.forms import forms


class APICall(forms.Form):

    def __init__(self, api_key=None, *args, **kwargs):
        super(APICall, self).__init__(*args, **kwargs)
        self.api_key = api_key

    def add_error(self, error, field=forms.NON_FIELD_ERRORS):
        if django.VERSION[:2] > (1, 6):
            error, field = field, error
            super(APICall, self).add_error(field, error)
        else:
            self._errors.setdefault(field, self.error_class()).append(error)

    def clean(self):
        for name, data in self.cleaned_data.items():
            setattr(self, name, data)
        return super(APICall, self).clean()

    def action(self, test):
        raise NotImplementedError('APIForms must implement action(self, test)')
