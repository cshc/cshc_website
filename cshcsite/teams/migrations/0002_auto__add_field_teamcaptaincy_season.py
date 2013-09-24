# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TeamCaptaincy.season'
        db.add_column(u'teams_teamcaptaincy', 'season',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Season'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TeamCaptaincy.season'
        db.delete_column(u'teams_teamcaptaincy', 'season_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.cshcuser': {
            'Meta': {'ordering': "['first_name', 'last_name']", 'object_name': 'CshcUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'members.member': {
            'Meta': {'ordering': "['first_name', 'last_name']", 'object_name': 'Member'},
            'first_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100'}),
            'pref_position': ('django.db.models.fields.IntegerField', [], {'default': '9'}),
            'profile_pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'shirt_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.CshcUser']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
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
        'teams.clubteamseasonparticipation': {
            'Meta': {'unique_together': "(('team', 'season'),)", 'object_name': 'ClubTeamSeasonParticipation'},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Cup']", 'null': 'True', 'blank': 'True'}),
            'cup_result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Division']", 'null': 'True'}),
            'division_fixtures_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'division_result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'division_tables_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'final_pos': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Season']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.ClubTeam']"}),
            'team_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'team_photo_caption': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'teams.southerner': {
            'Meta': {'ordering': "['season', 'avg_points_per_game']", 'unique_together': "(('team', 'season'),)", 'object_name': 'Southerner'},
            'avg_points_per_game': ('django.db.models.fields.FloatField', [], {}),
            'bonus_points': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'drawn': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'goals_against': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'goals_for': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lost': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'result_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Season']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.ClubTeam']"}),
            'won': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'teams.teamcaptaincy': {
            'Meta': {'ordering': "['-start']", 'object_name': 'TeamCaptaincy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_vice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Season']", 'null': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.ClubTeam']"})
        }
    }

    complete_apps = ['teams']