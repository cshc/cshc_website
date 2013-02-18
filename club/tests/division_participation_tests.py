from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date
from club.models import League, Division, Season, DivisionSeason, Team, Club, DivisionParticipation
from club.models.choices import *

class DivisionParticipationTest(TestCase):

    def setUp(self):
        self.test_url = "http://www.cambridgesouthhockeyclub.co.uk"
        self.test_club = Club(name="Cambridge South", website=self.test_url)
        self.test_club.save()
        self.test_team1 = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        self.test_team1.save()
        self.test_team2 = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T2)
        self.test_team2.save()
        self.test_league = League(name="Test League", url=self.test_url)
        self.test_league.save()
        self.test_div = Division(name="Test Division", league=self.test_league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        self.test_div.save()
        self.test_season = Season(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_season.save()
        self.test_div_season = DivisionSeason(division=self.test_div, season=self.test_season)
        self.test_div_season.save()

    def test_division_participations_can_be_added_and_removed(self):
        """ Tests that division participations can be added to the database and then removed """
        div_part1 = DivisionParticipation(team=self.test_team1, div_season=self.test_div_season, final_pos=1)
        div_part2 = DivisionParticipation(team=self.test_team2, div_season=self.test_div_season, final_pos=2)
        div_part1.save()
        div_part2.save()
        self.assertEqual(2, DivisionParticipation.objects.all().count())
        div_part1.delete()
        div_part2.delete()
        self.assertEqual(0, DivisionParticipation.objects.all().count())

    def test_duplicate_division_participations_are_not_allowed(self):
        """ Tests that the combination of division season and a team must be unique """
        div_part1 = DivisionParticipation(team=self.test_team1, div_season=self.test_div_season)
        div_part2 = DivisionParticipation(team=div_part1.team, div_season=div_part1.div_season)
        div_part1.save()
        self.assertRaises(IntegrityError, div_part2.save)

    def test_division_participation_final_position_is_optional(self):
        """ Tests that the final position of the division participation can be unset when saving """
        div_part = DivisionParticipation(team=self.test_team1, div_season=self.test_div_seaso)
        self.assertEqual(None, div_part.final_pos)
        div_part.save()
        self.assertEqual(1, DivisionParticipation.objects.all().count())