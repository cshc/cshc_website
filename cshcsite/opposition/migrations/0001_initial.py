# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Club'
        db.create_table(u'opposition_club', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=255)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('kit_clash_men', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('kit_clash_ladies', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('kit_clash_mixed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('default_venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venues.Venue'], null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('opposition', ['Club'])

        # Adding model 'Team'
        db.create_table(u'opposition_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teams', to=orm['opposition.Club'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('opposition', ['Team'])

        # Adding model 'ClubStats'
        db.create_table(u'opposition_clubstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.ClubTeam'], null=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opposition.Club'])),
            ('home_won', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('home_drawn', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('home_lost', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('home_gf', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('home_ga', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('away_won', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('away_drawn', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('away_lost', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('away_gf', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('away_ga', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('opposition', ['ClubStats'])


    def backwards(self, orm):
        # Deleting model 'Club'
        db.delete_table(u'opposition_club')

        # Deleting model 'Team'
        db.delete_table(u'opposition_team')

        # Deleting model 'ClubStats'
        db.delete_table(u'opposition_clubstats')


    models = {
        'opposition.club': {
            'Meta': {'ordering': "['name']", 'object_name': 'Club'},
            'default_venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['venues.Venue']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kit_clash_ladies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kit_clash_men': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kit_clash_mixed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'opposition.clubstats': {
            'Meta': {'ordering': "['club', 'team']", 'object_name': 'ClubStats'},
            'away_drawn': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'away_ga': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'away_gf': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'away_lost': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'away_won': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opposition.Club']"}),
            'home_drawn': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'home_ga': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'home_gf': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'home_lost': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'home_won': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.ClubTeam']", 'null': 'True'})
        },
        'opposition.team': {
            'Meta': {'ordering': "['club', 'name']", 'object_name': 'Team'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': "orm['opposition.Club']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'teams.clubteam': {
            'Meta': {'ordering': "['position']", 'object_name': 'ClubTeam'},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fill_blanks': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'ordinal': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'personal_stats': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'rivals': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'southerners': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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

    complete_apps = ['opposition']