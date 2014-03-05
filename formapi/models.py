# coding=utf-8
from django.db import models
from .fields import UUIDField


class APIKey(models.Model):
    email = models.EmailField(blank=False, null=False)
    key = UUIDField()
    secret = UUIDField()
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
