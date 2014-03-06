# coding=utf-8
from django.contrib import admin
from .models import APIKey


class APIKeyAdmin(admin.ModelAdmin):
    readonly_fields = ('key', 'secret')
    list_display = ('id', 'email', 'revoked', 'test', 'created')

admin.site.register(APIKey, APIKeyAdmin)
