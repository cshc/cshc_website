import logging
from django.test import TestCase
from ..models import Member

log = logging.getLogger(__name__)


class MemberTest(TestCase):
    """Tests for the Member model"""

    def setUp(self):
        self.test_member = Member(first_name="Graham", last_name="McCulloch", gender=Member.GENDER.Male, pref_position=Member.POSITION.Fwd)

    def test_members_can_be_added_and_removed(self):
        """ Tests that members can be added to the database and then removed """
        countBefore = Member.objects.all().count()
        member1 = Member(first_name="Test 1", last_name="eafew", gender=Member.GENDER.Male, pref_position=Member.POSITION.Fwd)
        member2 = Member(first_name="Test 2", last_name="btrwhs", gender=Member.GENDER.Male, pref_position=Member.POSITION.Mid)
        member1.save()
        member2.save()
        self.assertEqual(countBefore + 2, Member.objects.all().count())
        member1.delete()
        member2.delete()
        self.assertEqual(countBefore, Member.objects.all().count())
