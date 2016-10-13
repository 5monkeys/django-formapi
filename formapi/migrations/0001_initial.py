# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

try:
    from south.db import db
    from south.v2 import SchemaMigration

except ImportError:
    try:
        from django.db import migrations, models
    except ImportError:
        raise Exception("South or Django>=1.8 is required")
    import formapi.fields


    class Migration(migrations.Migration):

        dependencies = [
        ]

        operations = [
            migrations.CreateModel(
                name='APIKey',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False,
                                            auto_created=True,
                                            primary_key=True)),
                    ('email', models.EmailField(max_length=254)),
                    ('key', formapi.fields.UUIDField(unique=True, max_length=32,
                                                     editable=False,
                                                     blank=True)),
                    ('secret',
                     formapi.fields.UUIDField(unique=True, max_length=32,
                                              editable=False, blank=True)),
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

else:
    from django.db import models


    class Migration(SchemaMigration):

        def forwards(self, orm):
            # Adding model 'APIKey'
            db.create_table('formapi_apikey', (
                ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
                ('key', self.gf('formapi.fields.UUIDField')(unique=True, max_length=32, blank=True)),
                ('secret', self.gf('formapi.fields.UUIDField')(unique=True, max_length=32, blank=True)),
                ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
                ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ))
            db.send_create_signal('formapi', ['APIKey'])


        def backwards(self, orm):
            # Deleting model 'APIKey'
            db.delete_table('formapi_apikey')


        models = {
            'formapi.apikey': {
                'Meta': {'object_name': 'APIKey'},
                'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
                'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
                'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
                'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
                'key': ('formapi.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
                'secret': ('formapi.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
            }
        }

        complete_apps = ['formapi']
