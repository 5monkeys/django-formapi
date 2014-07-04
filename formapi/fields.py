import os
import base64

from django.db import models


def key_generator(length):
    if length & 0b11:
        raise ValueError('key length must be multiple of 4')
    return lambda: base64.urlsafe_b64encode(os.urandom(length * 6 / 8))


class KeyField(models.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('unique', True)

        if 'default' not in kwargs:
            generated_key_length = kwargs.pop('generated_key_length', kwargs['max_length'])
            kwargs['default'] = key_generator(generated_key_length)
        elif 'generated_key_length' in kwargs:
            raise ValueError('generated_key_length and default cannot '
                             'be set simultaneously')

        super(KeyField, self).__init__(**kwargs)


# TODO Remove UUIDField. Remains for backward
# compatibility with South migrations.


import re
import uuid
from django import forms
from .utils import prepare_uuid_string


try:
    from psycopg2 import extras
    extras.register_uuid()
except (ImportError, AttributeError):
    pass


def uuid_validator(value):
    if re.search('[^a-f0-9]+', value):
        raise forms.ValidationError(u"Invalid UUID value")


class UUIDField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, **kwargs):
        kwargs.update(max_length=32, editable=False, blank=True, unique=True)
        super(UUIDField, self).__init__(**kwargs)

    def db_type(self, connection=None):
        if connection and 'postgres' in connection.vendor:
            return 'uuid'
        return 'char(%s)' % self.max_length

    def pre_save(self, model_instance, add):
        if add:
            value = uuid.uuid4().hex
            setattr(model_instance, self.attname, value)
        else:
            value = getattr(model_instance, self.attname, None)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        return prepare_uuid_string(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return prepare_uuid_string(value, default='')

    def to_python(self, value):
        return prepare_uuid_string(value)

    def formfield(self, **kwargs):
        kwargs.update(
            form_class=forms.CharField,
            max_length=self.max_length,
            min_length=self.max_length,
            validators=[
                uuid_validator,
                forms.validators.MaxLengthValidator,
                forms.validators.MinLengthValidator,
            ],
        )
        return super(UUIDField, self).formfield(**kwargs)


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], [r"^formapi\.fields\.(?:Key|UUID)Field"])
