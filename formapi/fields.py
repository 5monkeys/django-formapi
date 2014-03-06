# coding=utf-8
import re
import uuid
from django import forms
from django.db import models

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
        return str(value) if isinstance(value, uuid.UUID) else value or None

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return str(value or '')

    def to_python(self, value):
        return str(value) if value else None

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
    add_introspection_rules([], [r"^formapi\.fields\.UUIDField"])
except ImportError:
    pass
