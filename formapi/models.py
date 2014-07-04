# coding=utf-8

from django.db import models
from .fields import KeyField


class APIKey(models.Model):
    email = models.EmailField(blank=False, null=False)
    key = KeyField(max_length=32, generated_key_length=16, unique=True)
    secret = KeyField(max_length=32, unique=True)
    comment = models.TextField(blank=True, null=True)
    revoked = models.BooleanField(default=False)
    test = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    # TODO add manytomany versions

    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'

    def __unicode__(self):
        return u'API Key #%s' % self.id

