from django.test import TestCase
from django.db import IntegrityError
from club.models import Member
from club.models.choices import MemberGender, MemberPosition
from django.contrib.auth.models import User

class MemberTest(TestCase):

    def setUp(self):
        self.user1 = User(username="gm", first_name="Graham", last_name="McCulloch", email="test@test.com")
        self.user2 = User(username="nh", first_name="nathan", last_name="humphreys", email="test2@test.com")
        self.user1.save()
        self.user2.save()
        self.test_member = Member(user=self.user1, gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        
    def test_members_can_be_added_and_removed(self):
        """ Tests that members can be added to the database and then removed """
        countBefore = Member.objects.all().count()
        member1 = Member(user=self.user1, gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        member2 = Member(user=self.user2, gender=MemberGender.MALE, pref_position=MemberPosition.MIDFIELDER)
        member1.save()
        member2.save()
        self.assertEqual(countBefore + 2, Member.objects.all().count())
        member1.delete()
        member2.delete()
        self.assertEqual(countBefore, Member.objects.all().count())

