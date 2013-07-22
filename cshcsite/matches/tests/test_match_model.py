import logging
from django.test import TestCase
from django.db import IntegrityError
from datetime import date
from core.models import TeamGender, TeamOrdinal
from teams.models import ClubTeam, ClubTeamSeasonParticipation
from opposition.models import Team, Club
from venues.models import Venue
from competitions.models import Season, Division, Cup, League
from ..models import Match

log = logging.getLogger(__name__)


class MatchTest(TestCase):
    """Tests for the Match model"""

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_venue, v_created = Venue.objects.get_or_create(name="Venue 1", short_name="Ven1")
        self.test_their_club, c_created = Club.objects.get_or_create(name="Test Club 2", website=self.test_url)
        self.test_our_team, t1_created = ClubTeam.objects.get_or_create(short_name="Test1", long_name="Test team 1", gender=TeamGender.mens, ordinal=TeamOrdinal.T1, position=20)
        self.test_their_team, t2_created = Team.objects.get_or_create(club=self.test_their_club, gender=TeamGender.mens, name="Opp team 1", short_name="Opp1")
        self.test_season, s_created = Season.objects.get_or_create(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_league, l_created = League.objects.get_or_create(name="Test League", url=self.test_url)
        self.test_div, d_created = Division.objects.get_or_create(name="Test Division", league=self.test_league, gender=TeamGender.mens)
        self.test_cup, cup_created = Cup.objects.get_or_create(name="Test Cup", gender=TeamGender.mens)
        self.test_part, p_created = ClubTeamSeasonParticipation.objects.get_or_create(team=self.test_our_team, division=self.test_div, cup=self.test_cup, season=self.test_season)
        self.match_date_1 = date(2012, 10, 1)
        self.match_date_2 = date(2012, 10, 8)

    def test_matches_can_be_added_and_removed(self):
        """ Tests that matches can be added to the database and then removed """
        countBefore = Match.objects.all().count()
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.Friendly)
        match2 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.away, date=self.match_date_2, fixture_type=Match.FIXTURE_TYPE.Friendly)
        match1.save()
        match2.save()
        self.assertEqual(countBefore + 2, Match.objects.all().count())
        match1.delete()
        match2.delete()
        self.assertEqual(countBefore, Match.objects.all().count())

    def test_season_is_automatically_set_when_saved(self):
        """ Tests that the season attribute is automatically set based on the date attribute when a match is saved"""
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.Friendly)
        self.assertIsNone(match1.season_id)
        self.assertIsNotNone(self.test_season)
        self.assertGreaterEqual(match1.date, self.test_season.start, "Match date must be after the start of the season")
        self.assertLessEqual(match1.date, self.test_season.end, "Match date must be before the end of the season")
        match1.save()
        self.assertEqual(self.test_season, match1.season)


    def test_division_is_automatically_set_when_a_league_match_is_saved(self):
        """ Tests that the division attribute is automatically set based on the current division of our_team when a match is saved"""
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.League)
        self.assertIsNone(match1.division)
        self.assertIsNotNone(self.test_div)
        match1.save()
        self.assertEqual(self.test_div, match1.division)

    def test_cup_is_automatically_set_when_a_cup_match_is_saved(self):
        """ Tests that the cup attribute is automatically set based on the current cup tournament of our_team when a match is saved"""
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.Cup)
        self.assertIsNone(match1.cup)
        self.assertIsNotNone(self.test_cup)
        match1.save()
        self.assertEqual(self.test_cup, match1.cup)

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

    def test_cannot_save_a_walkover_match_with_an_invalid_score(self):
        """ Tests that if a match is marked as a walk-over, the score must be entered correctly"""
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.Friendly)
        match1.alt_outcome = Match.ALTERNATIVE_OUTCOME.Walkover
        match1.our_score = 2
        match1.opp_score = 1
        self.assertRaises(IntegrityError, match1.save)

    def test_scores_must_not_be_set_for_a_cancelled_or_postponed_match(self):
        """ Tests that if a match is marked as a cancelled or postponed, the scores must not be set"""
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.Friendly)

        match1.alt_outcome = Match.ALTERNATIVE_OUTCOME.Cancelled
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

        match1.alt_outcome = Match.ALTERNATIVE_OUTCOME.Postponed
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
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.Friendly)
        match1.save()
        match1.our_score = 2
        self.assertRaises(IntegrityError, match1.save)
        match1.our_score = None
        match1.opp_score = 2
        self.assertRaises(IntegrityError, match1.save)
        match1.opp_score = None

    def test_cant_specify_too_many_opposition_own_goals(self):
        """ Tests that the number of own goals must be less than or equal to the number of our goals """
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.Friendly)
        match1.opp_own_goals = 3
        match1.our_score = 2
        match1.opp_score = 1
        self.assertRaises(IntegrityError, match1.save)

    def test_half_time_scores_must_be_less_than_final_scores(self):
        """ Tests that you can't specify half-time scores that are greater than the full time scores """
        match1 = Match(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, date=self.match_date_1, fixture_type=Match.FIXTURE_TYPE.Friendly)
        match1.our_score = 1
        match1.opp_score = 1
        match1.our_ht_score = 2
        match1.opp_ht_score = 0
        self.assertTrue(match1.all_scores_provided())
        self.assertRaises(IntegrityError, match1.save)
        match1.our_ht_score = 0
        match1.opp_ht_score = 2
        self.assertRaises(IntegrityError, match1.save)

