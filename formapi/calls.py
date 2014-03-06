# coding=utf-8
from django.forms import forms


class APICall(forms.Form):

    def __init__(self, api_key=None, *args, **kwargs):
        super(APICall, self).__init__(*args, **kwargs)
        self.api_key = api_key

    def add_error(self, error_msg, field_name=forms.NON_FIELD_ERRORS):
        # TODO: with Django master you would just raise ValidationError({field_name: error_msg})
        self._errors.setdefault(field_name, self.error_class()).append(error_msg)

    def clean(self):
        for name, data in self.cleaned_data.items():
            setattr(self, name, data)
        return super(APICall, self).clean()

    def action(self, test):
        raise NotImplementedError('APIForms must implement action(self, test)')
