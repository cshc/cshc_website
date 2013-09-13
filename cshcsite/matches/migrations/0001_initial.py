# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Match'
        db.create_table(u'matches_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('our_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.ClubTeam'])),
            ('opp_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opposition.Team'])),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venues.Venue'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('home_away', self.gf('django.db.models.fields.CharField')(default='Home', max_length=5)),
            ('fixture_type', self.gf('django.db.models.fields.CharField')(default='League', max_length=10)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')(default=None, null=True, blank=True)),
            ('alt_outcome', self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True)),
            ('our_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
            ('opp_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
            ('our_ht_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
            ('opp_ht_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
            ('opp_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('pre_match_hype', self.gf('model_utils.fields.SplitField')(no_excerpt_field=True, blank=True)),
            ('report_title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('report_author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='match_reports', null=True, on_delete=models.SET_NULL, to=orm['members.Member'])),
            ('report_body', self.gf('model_utils.fields.SplitField')(no_excerpt_field=True, blank=True)),
            ('report_pub_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('ignore_for_goal_king', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ignore_for_southerners', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('override_kit_clash', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gpg_pro_rata', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Season'])),
            ('division', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Division'], null=True, on_delete=models.PROTECT, blank=True)),
            ('cup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Cup'], null=True, on_delete=models.PROTECT, blank=True)),
            (u'_pre_match_hype_excerpt', self.gf('django.db.models.fields.TextField')()),
            (u'_report_body_excerpt', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('matches', ['Match'])

        # Adding model 'Appearance'
        db.create_table(u'matches_appearance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='appearances', to=orm['members.Member'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(related_name='appearances', to=orm['matches.Match'])),
            ('goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('green_card', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('yellow_card', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('red_card', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('matches', ['Appearance'])

        # Adding unique constraint on 'Appearance', fields ['member', 'match']
        db.create_unique(u'matches_appearance', ['member_id', 'match_id'])

        # Adding model 'GoalKing'
        db.create_table(u'matches_goalking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Season'])),
            ('games_played', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m1_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m2_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m3_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m4_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m5_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('l1_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('l2_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('mixed_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('indoor_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m1_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m2_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m3_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m4_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('m5_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('l1_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('l2_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('mixed_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('indoor_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('total_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('total_own_goals', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('matches', ['GoalKing'])

        # Adding unique constraint on 'GoalKing', fields ['member', 'season']
        db.create_unique(u'matches_goalking', ['member_id', 'season_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'GoalKing', fields ['member', 'season']
        db.delete_unique(u'matches_goalking', ['member_id', 'season_id'])

        # Removing unique constraint on 'Appearance', fields ['member', 'match']
        db.delete_unique(u'matches_appearance', ['member_id', 'match_id'])

        # Deleting model 'Match'
        db.delete_table(u'matches_match')

        # Deleting model 'Appearance'
        db.delete_table(u'matches_appearance')

        # Deleting model 'GoalKing'
        db.delete_table(u'matches_goalking')


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
        'matches.goalking': {
            'Meta': {'ordering': "['season', 'member']", 'unique_together': "(('member', 'season'),)", 'object_name': 'GoalKing'},
            'games_played': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indoor_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'indoor_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'l1_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'l1_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'l2_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'l2_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm1_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm1_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm2_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm2_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm3_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm3_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm4_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm4_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm5_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'm5_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'mixed_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'mixed_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competitions.Season']"}),
            'total_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'total_own_goals': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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

    complete_apps = ['matches']