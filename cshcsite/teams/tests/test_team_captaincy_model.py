import logging
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from core.models import TeamGender, TeamOrdinal
from members.models import Member
from ..models import ClubTeam, TeamCaptaincy

log = logging.getLogger(__name__)


class TeamCaptaincyTest(TestCase):
    """Tests for the TeamCaptaincy model"""

    def setUp(self):
        self.user1, u1_created = User.objects.get_or_create(username="gm", first_name="Graham", last_name="McCulloch", email="test@test.com")
        self.user2, u1_created = User.objects.get_or_create(username="nh", first_name="Nathan", last_name="McCulloch", email="test2@test.com")
        self.test_member1, m1_created = Member.objects.get_or_create(user=self.user1, gender=Member.GENDER.Male, pref_position=Member.POSITION.Fwd)
        self.test_member2, m2_created = Member.objects.get_or_create(user=self.user2, gender=Member.GENDER.Male, pref_position=Member.POSITION.Fwd)
        self.test_url = "http://www.example.com"
        self.test_team, t_created = ClubTeam.objects.get_or_create(gender=TeamGender.mens, ordinal=TeamOrdinal.T1)

    def test_team_captaincies_can_be_added_and_removed(self):
        """ Tests that team captaincies can be added to the database and then removed """
        countBefore = TeamCaptaincy.objects.all().count()
        tc1 = TeamCaptaincy(member=self.test_member1, team=self.test_team, start=date.today())
        tc2 = TeamCaptaincy(member=self.test_member2, team=self.test_team, start=date.today(), is_vice=True)
        tc1.save()
        tc2.save()
        self.assertEqual(countBefore + 2, TeamCaptaincy.objects.all().count())
        tc1.delete()
        tc2.delete()
        self.assertEqual(countBefore, TeamCaptaincy.objects.all().count())
