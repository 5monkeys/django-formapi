from django.forms import forms


class APICall(forms.Form):

    def __init__(self, api_key=None, *args, **kwargs):
        super(APICall, self).__init__(*args, **kwargs)
        self.api_key = api_key

    def add_error(self, error_msg):
        errors = self.non_field_errors()
        errors.append(error_msg)
        self._errors[forms.NON_FIELD_ERRORS] = errors

    def clean(self):
        for name, data in self.cleaned_data.iteritems():
            setattr(self, name, data)
        return super(APICall, self).clean()

    def action(self, test):
        raise NotImplementedError('APIForms must implement action(self, test)')
