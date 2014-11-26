# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MatchComment'
        db.create_table(u'commentary_matchcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='match_comments', null=True, on_delete=models.SET_NULL, to=orm['core.CshcUser'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_comments', to=orm['matches.Match'])),
            ('comment_type', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='Approved', max_length=10)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('commentary', ['MatchComment'])

        # Adding model 'MatchCommentator'
        db.create_table(u'commentary_matchcommentator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('commentator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_commentries', to=orm['core.CshcUser'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_commentator', unique=True, to=orm['matches.Match'])),
        ))
        db.send_create_signal('commentary', ['MatchCommentator'])


    def backwards(self, orm):
        # Deleting model 'MatchComment'
        db.delete_table(u'commentary_matchcomment')

        # Deleting model 'MatchCommentator'
        db.delete_table(u'commentary_matchcommentator')


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
        'commentary.matchcomment': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'MatchComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'match_comments'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['core.CshcUser']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comment_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_comments'", 'to': "orm['matches.Match']"}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'Approved'", 'max_length': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'commentary.matchcommentator': {
            'Meta': {'ordering': "['-match']", 'object_name': 'MatchCommentator'},
            'commentator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_commentries'", 'to': "orm['core.CshcUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_commentator'", 'unique': 'True', 'to': "orm['matches.Match']"})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        'matches.appearance': {
            'Meta': {'ordering': "['match', 'member']", 'unique_together': "(('member', 'match'),)", 'object_name': 'Appearance'},
            'goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'green_card': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appearances'", 'to': "orm['matches.Match']"}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appearances'", 'to': "orm['members.Member']"}),
            'own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'red_card': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'yellow_card': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'matches.match': {
            'Meta': {'ordering': "['date']", 'object_name': 'Match'},
            u'_pre_match_hype_excerpt': ('django.db.models.fields.TextField', [], {}),
            u'_report_body_excerpt': ('django.db.models.fields.TextField', [], {}),
            'alt_outcome': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'cup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Cup']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Division']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'fixture_type': ('django.db.models.fields.CharField', [], {'default': "'League'", 'max_length': '10'}),
            'gpg_pro_rata': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'home_away': ('django.db.models.fields.CharField', [], {'default': "'Home'", 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_for_goal_king': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ignore_for_southerners': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'opp_ht_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'opp_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'opp_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'opp_team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opposition.Team']"}),
            'our_ht_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'our_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'our_team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.ClubTeam']"}),
            'override_kit_clash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'matches'", 'symmetrical': 'False', 'through': "orm['matches.Appearance']", 'to': "orm['members.Member']"}),
            'pre_match_hype': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'report_author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'match_reports'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['members.Member']"}),
            'report_body': ('model_utils.fields.SplitField', [], {u'no_excerpt_field': 'True', 'blank': 'True'}),
            'report_pub_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'report_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Season']"}),
            'time': ('django.db.models.fields.TimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['venues.Venue']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
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

    complete_apps = ['commentary']