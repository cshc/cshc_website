from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date, time
from club.models import *
from club.models.choices import *

class MatchTest(TestCase):

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_venue = Venue(name="Venue 1", short_name="Ven1")
        self.test_our_club = Club(name="Test Club 1", website="http://www.cambridgesouthhockeyclub.co.uk")
        self.test_our_club.save()
        self.test_their_club = Club(name="Test Club 2", website="http://www.cambridgecityhc.org/")
        self.test_their_club.save()
        self.test_our_team = Team(club=self.test_our_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        self.test_our_team.save()
        self.test_their_team = Team(club=self.test_their_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        self.test_their_team.save()
        self.test_league = League(name="Test League", url=self.test_url)
        self.test_league.save()
        self.test_div = Division(name="Test Division", league=self.test_league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        self.test_div.save()
        self.test_season = Season(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_season.save()
        self.test_div_season = DivisionSeason(division=self.test_div, season=self.test_season)
        self.test_div_season.save()
        self.test_cup = Cup(name="Test cup")
        self.test_cup.save()
        self.test_cup_season = CupSeason(cup=self.test_cup, season=self.test_season)
        self.test_cup_season.save()


class FriendlyMatchTest(MatchTest):

    def test_friendly_matches_can_be_added_and_removed(self):
        """ Tests that friendly matches can be added to the database and then removed """
        countBeforeMatch = Match.objects.all().count()
        countBeforeFriendly = FriendlyMatch.objects.all().count()
        match1 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        match2 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.AWAY, date=date(2012, 10, 8), season=self.test_season)
        match1.save()
        match2.save()
        self.assertEqual(countBeforeMatch + 2, Match.objects.all().count())
        self.assertEqual(countBeforeFriendly + 2, FriendlyMatch.objects.all().count())
        match1.delete()
        match2.delete()
        self.assertEqual(countBeforeMatch, Match.objects.all().count())
        self.assertEqual(countBeforeFriendly, FriendlyMatch.objects.all().count())

    def test_is_walkover_score(self):
        """ Tests that the is_walkover_score method logic is correct """
        self.assertTrue(Match.is_walkover_score(3, 0))
        self.assertTrue(Match.is_walkover_score(5, 0))
        self.assertTrue(Match.is_walkover_score(0, 3))
        self.assertTrue(Match.is_walkover_score(0, 5))
        self.assertFalse(Match.is_walkover_score(2, 1))
        self.assertFalse(Match.is_walkover_score(0, 0))
        self.assertFalse(Match.is_walkover_score(3, 3))
        self.assertFalse(Match.is_walkover_score(5, 5))
        self.assertEqual("3-0, 5-0, 0-3 or 0-5", Match.valid_walkover_scores())
        
    def test_a_team_cannot_play_itself(self):
        """ Tests that you cannot set the our_team and opp_team attributes to the same Team """
        match1 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_our_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        self.assertRaises(IntegrityError, match1.save)
        
    def test_cannot_save_a_walkover_match_with_an_invalid_score(self):
        """ Tests that if a match is marked as a walk-over, the score must be entered correctly"""
        match1 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        match1.alt_outcome = AlternativeOutcome.WALKOVER
        match1.our_score = 2
        match1.opp_score = 1
        self.assertRaises(IntegrityError, match1.save)

    def test_scores_must_not_be_set_for_a_cancelled_or_postponed_match(self):
        """ Tests that if a match is marked as a cancelled or postponed, the scores must not be set"""
        match1 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        
        match1.alt_outcome = AlternativeOutcome.CANCELLED
        match1.our_score = 1
        match1.opp_score = 1
        self.assertTrue(match1.final_scores_provided())
        self.assertRaises(IntegrityError, match1.save)
        match1.our_score = None
        match1.opp_score = None
        
        match1.our_ht_score = 1
        match1.opp_ht_score = 1
        self.assertTrue(match1.ht_scores_provided())
        self.assertRaises(IntegrityError, match1.save)
        match1.our_ht_score = None
        match1.opp_ht_score = None
        
        match1.alt_outcome = AlternativeOutcome.POSTPONED
        match1.our_score = 1
        match1.opp_score = 1
        self.assertTrue(match1.final_scores_provided())
        self.assertRaises(IntegrityError, match1.save)
        match1.our_score = None
        match1.opp_score = None
        
        match1.our_ht_score = 1
        match1.opp_ht_score = 1
        self.assertTrue(match1.ht_scores_provided())
        self.assertRaises(IntegrityError, match1.save)
        match1.our_ht_score = None
        match1.opp_ht_score = None
        
    def test_cannot_provide_just_one_score(self):
        """ Tests that you must provide both scores, not just one of them """
        match1 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        match1.save()
        match1.our_score = 2
        self.assertRaises(IntegrityError, match1.save)
        match1.our_score = None
        match1.opp_score = 2
        self.assertRaises(IntegrityError, match1.save)
        match1.opp_score = None
        
    def test_cant_specify_too_many_opposition_own_goals(self):
        """ Tests that the number of own goals must be less than or equal to the number of our goals """
        match1 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        match1.opp_own_goals = 3
        match1.our_score = 2
        match1.opp_score = 1
        self.assertRaises(IntegrityError, match1.save)        
        
    def test_half_time_scores_must_be_less_than_final_scores(self):
        """ Tests that you can't specify half-time scores that are greater than the full time scores """
        match1 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        match1.our_score = 1
        match1.opp_score = 1
        match1.our_ht_score = 2
        match1.opp_ht_score = 0
        self.assertTrue(match1.all_scores_provided())
        self.assertRaises(IntegrityError, match1.save)    
        match1.our_ht_score = 0
        match1.opp_ht_score = 2
        self.assertRaises(IntegrityError, match1.save)
        
class CupMatchTest(MatchTest):

    def test_cup_matches_can_be_added_and_removed(self):
        """ Tests that cup_matches can be added to the database and then removed """
        countBeforeMatch = Match.objects.all().count()
        countBeforeCup = CupMatch.objects.all().count()
        match1 = CupMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), cup_season=self.test_cup_season)
        match2 = CupMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.AWAY, date=date(2012, 10, 8), cup_season=self.test_cup_season)
        match1.time = time(10, 5, 30)
        dt = match1.datetime()
        match1.save()
        match2.save()
        self.assertEqual(countBeforeMatch + 2, Match.objects.all().count())
        self.assertEqual(countBeforeCup + 2, CupMatch.objects.all().count())
        match1.delete()
        match2.delete()
        self.assertEqual(countBeforeMatch, Match.objects.all().count())
        self.assertEqual(countBeforeCup, CupMatch.objects.all().count())


class DivisionMatchTest(MatchTest):

    def test_division_matches_can_be_added_and_removed(self):
        """ Tests that division matches can be added to the database and then removed """
        countBeforeMatch = Match.objects.all().count()
        countBeforeDiv = DivisionMatch.objects.all().count()
        match1 = DivisionMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), div_season=self.test_div_season)
        match2 = DivisionMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.AWAY, date=date(2012, 10, 8), div_season=self.test_div_season)
        match1.save()
        match2.save()
        self.assertEqual(countBeforeMatch + 2, Match.objects.all().count())
        self.assertEqual(countBeforeDiv + 2, DivisionMatch.objects.all().count())
        match1.delete()
        match2.delete()
        self.assertEqual(countBeforeMatch, Match.objects.all().count())
        self.assertEqual(countBeforeDiv, DivisionMatch.objects.all().count())