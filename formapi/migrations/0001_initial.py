# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import formapi.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('key', formapi.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('secret', formapi.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('revoked', models.BooleanField(default=False)),
                ('test', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'API Key',
                'verbose_name_plural': 'API Keys',
            },
        ),
    ]
