# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Venue'
        db.create_table(u'venues_venue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=255)),
            ('short_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('is_home', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('addr1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('addr2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('addr3', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('addr_city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('addr_postcode', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('distance', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
        ))
        db.send_create_signal('venues', ['Venue'])


    def backwards(self, orm):
        # Deleting model 'Venue'
        db.delete_table(u'venues_venue')


    models = {
        'venues.venue': {
            'Meta': {'ordering': "['name']", 'object_name': 'Venue'},
            'addr1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'addr2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'addr3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'addr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'addr_postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'distance': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['venues']