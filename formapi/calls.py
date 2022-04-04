# coding=utf-8
import warnings
import django
from django.forms import forms


class APICall(forms.Form):
    def __init__(self, api_key=None, *args, **kwargs):
        super(APICall, self).__init__(*args, **kwargs)
        self.api_key = api_key

    def add_error(self, error_msg, field_name=forms.NON_FIELD_ERRORS):
        if django.VERSION >= (1, 7):
            if isinstance(field_name, forms.ValidationError):
                field, error = error_msg, field_name
            else:
                warnings.warn(
                    "%s.add_error arguments should be (field, error) "
                    "for Django 1.7+ and instead of using .add_error() one "
                    "can just simply raise ValidationError({field_name: "
                    "error_message})" % (self.__class__,),
                    DeprecationWarning,
                )
                error, field = error_msg, field_name
            super(APICall, self).add_error(field, error)
        else:
            self._errors.setdefault(field_name, self.error_class()).append(error_msg)

    def clean(self):
        for name, data in self.cleaned_data.items():
            setattr(self, name, data)
        return super(APICall, self).clean()

    def action(self, test):
        raise NotImplementedError("APIForms must implement action(self, test)")
