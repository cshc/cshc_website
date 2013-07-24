import logging
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from datetime import date
from core.models import TeamGender, TeamOrdinal
from teams.models import ClubTeam
from opposition.models import Team, Club
from members.models import Member
from venues.models import Venue
from competitions.models import Season
from ..models import Match, Appearance

log = logging.getLogger(__name__)


class AppearanceTest(TestCase):
    """Tests for the Appearance model"""

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_venue, v_created = Venue.objects.get_or_create(name="Venue 1", short_name="Ven1")
        self.test_their_club, c_created = Club.objects.get_or_create(name="Test Club 2", website=self.test_url)
        self.test_our_team, t1_created = ClubTeam.objects.get_or_create(short_name="Test1", long_name="Test team 1", gender=TeamGender.Mens, ordinal=TeamOrdinal.T1, position=20)
        self.test_their_team, t2_created = Team.objects.get_or_create(club=self.test_their_club, gender=TeamGender.Mens, name="Opp team 1", short_name="Opp1")
        self.test_season, s_created = Season.objects.get_or_create(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_match, m_created = Match.objects.get_or_create(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.Home, fixture_type=Match.FIXTURE_TYPE.Friendly, date=date(2012, 10, 1))
        self.test_member1, m1_created = Member.objects.get_or_create(first_name="Graham", last_name="McCulloch", gender=Member.GENDER.Male, pref_position=Member.POSITION.Fwd)
        self.test_member2, m2_created = Member.objects.get_or_create(first_name="Nathan", last_name="Humphreys", gender=Member.GENDER.Male, pref_position=Member.POSITION.Mid)

    def test_appearances_can_be_added_and_removed(self):
        """ Tests that appearances can be added to the database and then removed """
        countBefore = Appearance.objects.all().count()
        app1 = Appearance(member=self.test_member1, match=self.test_match, goals=3, own_goals=0)
        app2 = Appearance(member=self.test_member2, match=self.test_match, goals=0, own_goals=3)
        app1.save()
        app2.save()
        self.assertEqual(countBefore + 2, Appearance.objects.all().count())
        app1.delete()
        app2.delete()
        self.assertEqual(countBefore, Appearance.objects.all().count())

    def test_a_member_cannot_appear_in_a_match_more_than_once(self):
        """"Tests that duplicate entries in the Appearances table are not allowed """
        app1 = Appearance(member=self.test_member1, match=self.test_match)
        app2 = Appearance(member=app1.member, match=app1.match)
        app1.save()
        self.assertRaises(IntegrityError, app2.save)
