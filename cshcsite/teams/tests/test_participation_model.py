import logging
from django.test import TestCase
from django.db import IntegrityError
from datetime import date
from core.models import TeamGender, TeamOrdinal
from competitions.models import Division, League, Season, Cup
from ..models import ClubTeam, ClubTeamSeasonParticipation

log = logging.getLogger(__name__)


class ClubTeamSeasonParticipationTest(TestCase):
    """Tests for the ClubTeamSeasonParticipation model"""

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_team1, t1_created = ClubTeam.objects.get_or_create(gender=TeamGender.mens, ordinal=TeamOrdinal.T1)
        self.test_team2, t2_created = ClubTeam.objects.get_or_create(gender=TeamGender.mens, ordinal=TeamOrdinal.T2)
        self.test_league, l_created = League.objects.get_or_create(name="Test League", url=self.test_url)
        self.test_div, d_created = Division.objects.get_or_create(name="Test Division", league=self.test_league, gender=TeamGender.mens)
        self.test_cup, c_created = Cup.objects.get_or_create(name="Test Cup")
        self.test_season, s_created = Season.objects.get_or_create(start=date(2012, 9, 1), end=date(2013, 8, 31))

    def test_clubteam_season_participations_can_be_added_and_removed(self):
        """ Tests that division participations can be added to the database and then removed """
        countBefore = ClubTeamSeasonParticipation.objects.all().count()
        participation1 = ClubTeamSeasonParticipation(team=self.test_team1, season=self.test_season)
        participation2 = ClubTeamSeasonParticipation(team=self.test_team2, season=self.test_season)
        participation1.save()
        participation2.save()
        self.assertEqual(countBefore + 2, ClubTeamSeasonParticipation.objects.all().count())
        participation1.delete()
        participation2.delete()
        self.assertEqual(countBefore, ClubTeamSeasonParticipation.objects.all().count())

    def test_duplicate_clubteam_season_participations_are_not_allowed(self):
        """ Tests that the combination of division season and a team must be unique """
        participation1 = ClubTeamSeasonParticipation(team=self.test_team1, season=self.test_season)
        participation2 = ClubTeamSeasonParticipation(team=participation1.team, season=participation1.season)
        participation1.save()
        self.assertRaises(IntegrityError, participation2.save)

