from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date
from club.models import Cup, Season, CupSeason, Team, Club, CupParticipation
from club.models.choices import *

class CupParticipationTest(TestCase):

    def setUp(self):
        self.test_url = "http://www.cambridgesouthhockeyclub.co.uk"
        self.test_club = Club(name="Cambridge South", website=self.test_url)
        self.test_club.save()
        self.test_team1 = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        self.test_team1.save()
        self.test_team2 = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T2)
        self.test_team2.save()
        self.test_cup = Cup(name="Test Cup")
        self.test_cup.save()
        self.test_season = Season(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_season.save()
        self.test_cup_season = CupSeason(cup=self.test_cup, season=self.test_season)
        self.test_cup_season.save()

    def test_cup_participations_can_be_added_and_removed(self):
        """ Tests that cup participations can be added to the database and then removed """
        cup_part1 = CupParticipation(team=self.test_team1, cup_season=self.test_cup_season)
        cup_part2 = CupParticipation(team=self.test_team2, cup_season=self.test_cup_season)
        cup_part1.save()
        cup_part2.save()
        self.assertEqual(2, CupParticipation.objects.all().count())
        cup_part1.delete()
        cup_part2.delete()
        self.assertEqual(0, CupParticipation.objects.all().count())

    def test_duplicate_cup_participations_are_not_allowed(self):
        """ Tests that the combination of cup season and a team must be unique """
        cup_part1 = CupParticipation(team=self.test_team1, cup_season=self.test_cup_season)
        cup_part2 = CupParticipation(team=cup_part1.team, cup_season=cup_part1.cup_season)
        cup_part1.save()
        self.assertRaises(IntegrityError, cup_part2.save)

    def test_cup_participation_result_is_optional(self):
        """ Tests that the result of the cup participation can be unset when saving """
        cup_part = CupParticipation(team=self.test_team1, cup_season=self.test_cup_season)
        self.assertEqual(None, cup_part.result)
        cup_part.save()
        self.assertEqual(1, CupParticipation.objects.all().count())