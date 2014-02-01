# coding=utf-8
from django.db import models
from uuidfield import UUIDField
from .compat import unicode


class APIKey(models.Model):
    email = models.EmailField(blank=False, null=False)
    key = UUIDField(auto=True, version=4)
    secret = UUIDField(auto=True, version=4)
    comment = models.TextField(blank=True, null=True)
    revoked = models.BooleanField(default=False)
    test = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    # TODO add manytomany versions

    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'

    def __unicode__(self):
        return u''.join((u'API Key (#', unicode(self.id), u')'))
