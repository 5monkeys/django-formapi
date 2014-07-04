# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'APIKey.secret'
        db.alter_column('formapi_apikey', 'secret', self.gf('formapi.fields.KeyField')(max_length=32))

        # Changing field 'APIKey.key'
        db.alter_column('formapi_apikey', 'key', self.gf('formapi.fields.KeyField')(max_length=32))

    def backwards(self, orm):

        # Changing field 'APIKey.secret'
        db.alter_column('formapi_apikey', 'secret', self.gf('formapi.fields.UUIDField')(max_length=32, unique=True))

        # Changing field 'APIKey.key'
        db.alter_column('formapi_apikey', 'key', self.gf('formapi.fields.UUIDField')(max_length=32, unique=True))

    models = {
        'formapi.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'SW6jrl31y_n01Kid'", 'unique': 'True', 'max_length': '16'}),
            'revoked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'2ZZqP8MdpnqRtACcFieE9u3JcGE4MRKC'", 'unique': 'True', 'max_length': '32'}),
            'test': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['formapi']