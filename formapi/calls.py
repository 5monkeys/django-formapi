import warnings

from django.forms import forms


class APICall(forms.Form):
    def __init__(self, api_key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key

    def add_error(self, error_msg, field_name=forms.NON_FIELD_ERRORS):
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
        super().add_error(field, error)

    def clean(self):
        for name, data in self.cleaned_data.items():
            setattr(self, name, data)
        return super().clean()

    def action(self, test):
        raise NotImplementedError("APIForms must implement action(self, test)")
