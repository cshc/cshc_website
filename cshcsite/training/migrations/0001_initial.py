# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TrainingSession'
        db.create_table(u'training_trainingsession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venues.Venue'])),
            ('description', self.gf('django.db.models.fields.CharField')(default='Full club training', max_length=100)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration_mins', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=120)),
            ('status', self.gf('model_utils.fields.StatusField')(default='Scheduled', max_length=100, no_check_for_status=True)),
        ))
        db.send_create_signal('training', ['TrainingSession'])

        # Adding unique constraint on 'TrainingSession', fields ['description', 'datetime']
        db.create_unique(u'training_trainingsession', ['description', 'datetime'])


    def backwards(self, orm):
        # Removing unique constraint on 'TrainingSession', fields ['description', 'datetime']
        db.delete_unique(u'training_trainingsession', ['description', 'datetime'])

        # Deleting model 'TrainingSession'
        db.delete_table(u'training_trainingsession')


    models = {
        'training.trainingsession': {
            'Meta': {'ordering': "['datetime']", 'unique_together': "(('description', 'datetime'),)", 'object_name': 'TrainingSession'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'default': "'Full club training'", 'max_length': '100'}),
            'duration_mins': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'Scheduled'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['venues.Venue']"})
        },
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

    complete_apps = ['training']