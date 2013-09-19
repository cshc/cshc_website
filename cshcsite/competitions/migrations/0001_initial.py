# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'League'
        db.create_table(u'competitions_league', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('competitions', ['League'])

        # Adding model 'Division'
        db.create_table(u'competitions_division', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=255)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(related_name='divisions', to=orm['competitions.League'])),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('competitions', ['Division'])

        # Adding unique constraint on 'Division', fields ['name', 'league', 'gender']
        db.create_unique(u'competitions_division', ['name', 'league_id', 'gender'])

        # Adding model 'Season'
        db.create_table(u'competitions_season', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('competitions', ['Season'])

        # Adding model 'Cup'
        db.create_table(u'competitions_cup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=255)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.League'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('competitions', ['Cup'])

        # Adding model 'DivisionResult'
        db.create_table(u'competitions_divisionresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('our_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.ClubTeam'], null=True)),
            ('opp_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opposition.Team'], null=True)),
            ('division', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Division'])),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Season'])),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('played', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('won', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('drawn', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('lost', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('goals_for', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('goals_against', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('goal_difference', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('points', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('competitions', ['DivisionResult'])

        # Adding unique constraint on 'DivisionResult', fields ['season', 'division', 'position']
        db.create_unique(u'competitions_divisionresult', ['season_id', 'division_id', 'position'])


    def backwards(self, orm):
        # Removing unique constraint on 'DivisionResult', fields ['season', 'division', 'position']
        db.delete_unique(u'competitions_divisionresult', ['season_id', 'division_id', 'position'])

        # Removing unique constraint on 'Division', fields ['name', 'league', 'gender']
        db.delete_unique(u'competitions_division', ['name', 'league_id', 'gender'])

        # Deleting model 'League'
        db.delete_table(u'competitions_league')

        # Deleting model 'Division'
        db.delete_table(u'competitions_division')

        # Deleting model 'Season'
        db.delete_table(u'competitions_season')

        # Deleting model 'Cup'
        db.delete_table(u'competitions_cup')

        # Deleting model 'DivisionResult'
        db.delete_table(u'competitions_divisionresult')


    models = {
        'competitions.cup': {
            'Meta': {'ordering': "['name']", 'object_name': 'Cup'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.League']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '255'})
        },
        'competitions.division': {
            'Meta': {'ordering': "['league', 'gender', 'name']", 'unique_together': "(('name', 'league', 'gender'),)", 'object_name': 'Division'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'divisions'", 'to': "orm['competitions.League']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'})
        },
        'competitions.divisionresult': {
            'Meta': {'ordering': "('season', 'division', 'position')", 'unique_together': "(('season', 'division', 'position'),)", 'object_name': 'DivisionResult'},
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Division']"}),
            'drawn': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'goal_difference': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'goals_against': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'goals_for': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lost': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'opp_team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opposition.Team']", 'null': 'True'}),
            'our_team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.ClubTeam']", 'null': 'True'}),
            'played': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Season']"}),
            'won': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'competitions.league': {
            'Meta': {'ordering': "['name']", 'object_name': 'League'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'competitions.season': {
            'Meta': {'ordering': "['start']", 'object_name': 'Season'},
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
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

    complete_apps = ['competitions']