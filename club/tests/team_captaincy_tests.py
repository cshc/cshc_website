from django.test import TestCase
from django.db import IntegrityError
from club.models import Club, Team, Member, TeamCaptaincy
from club.models.choices import *
from datetime import datetime, date

class TeamCaptaincyTest(TestCase):

    def setUp(self):
        self.test_member1 = Member(first_name="Graham", surname="McCulloch", gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        self.test_member1.save()
        self.test_member2 = Member(first_name="Mark", surname="Williams", gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        self.test_member2.save()
        self.test_url = "http://www.example.com"
        self.test_club = Club(name="Cambridge South", website=self.test_url)
        self.test_club.save()
        self.test_team = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        self.test_team.save()

    def test_team_captaincies_can_be_added_and_removed(self):
        """ Tests that team captaincies can be added to the database and then removed """
        tc1 = TeamCaptaincy(member=self.test_member1, team=self.test_team, start=date.today())
        tc2 = TeamCaptaincy(member=self.test_member2, team=self.test_team, start=date.today(), is_vice=True)
        tc1.save()
        tc2.save()
        self.assertEqual(2, TeamCaptaincy.objects.all().count())
        tc1.delete()
        tc2.delete()
        self.assertEqual(0, TeamCaptaincy.objects.all().count())