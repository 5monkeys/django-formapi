# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
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