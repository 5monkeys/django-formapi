from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from formapi import calls
from formapi.api import API


class AuthenticateUserCall(calls.APICall):
    """
    Authenticate a user
    """

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. "
            "Note that both fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the label for the "username" field.
        self.username_field = User._meta.get_field("username")

    def action(self, test):
        return self.get_user_id()

    def clean(self):
        super().clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"]
                    % {"username": self.username_field.verbose_name}
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages["inactive"])
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class DivisionCall(calls.APICall):
    """
    Returns the quotient of two integers
    """

    dividend = forms.IntegerField()
    divisor = forms.IntegerField()

    signed_requests = False

    def action(self, test):
        dividend = self.cleaned_data.get("dividend")
        divisor = self.cleaned_data.get("divisor")
        try:
            return float(dividend) / float(divisor)
        except ZeroDivisionError:
            self.add_error("DIVISION BY ZERO, OH SHIIIIII")


class ProgrammingLanguages(calls.APICall):
    RUBY = "ruby"
    PYTHON = "python"
    JAVA = "java"
    LANGUAGES = ((RUBY, "Freshman"), (PYTHON, "Sophomore"), (JAVA, "Junior"))
    languages = forms.MultipleChoiceField(choices=LANGUAGES)

    def action(self, test):
        return "Good for you"


API.register(AuthenticateUserCall, "user", "authenticate", version="v1.0.0")
API.register(DivisionCall, "math", "divide", version="v1.0.0")
API.register(ProgrammingLanguages, "comp", "lang", version="v1.0.0")
