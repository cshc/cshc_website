from django.test import TestCase
from django.db import IntegrityError
from club.models import Member
from club.models.choices import MemberGender, MemberPosition

class MemberTest(TestCase):

    def setUp(self):
        self.test_member = Member(first_name="Graham", surname="McCulloch", gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        
    def test_members_can_be_added_and_removed(self):
        """ Tests that members can be added to the database and then removed """
        member1 = Member(first_name="Graham", surname="McCulloch", gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        member2 = Member(first_name="Mark", surname="Williams", gender=MemberGender.MALE, pref_position=MemberPosition.MIDFIELDER)
        member1.save()
        member2.save()
        self.assertEqual(2, Member.objects.all().count())
        member1.delete()
        member2.delete()
        self.assertEqual(0, Member.objects.all().count())

    def test_member_first_name_and_surname_must_be_specified(self):
        """ Tests that you must specify the first name and surname of the member """
        member_with_no_first_name = Member(surname="McCulloch", gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        self.assertEqual(None, member_with_no_first_name.first_name)
        self.assertRaisesMessage(IntegrityError, "club_member.first_name may not be NULL", member_with_no_first_name.save)
        member_with_no_surname = Member(first_name="Graham", gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        self.assertEqual(None, member_with_no_surname.surname)
        self.assertRaisesMessage(IntegrityError, "club_member.surname may not be NULL", member_with_no_surname.save)


    def test_multiple_members_can_have_the_same_first_name_and_surname(self):
        """ 
        Tests that its possible to have multiple members with the same first name and surname. 
        Note that this may make it very hard to select the right member!

        """
        member1 = Member(first_name="Graham", surname="McCulloch", gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        member2 = Member(first_name=member1.first_name, surname=member1.surname, gender=MemberGender.MALE, pref_position=MemberPosition.MIDFIELDER)
        member1.save()
        member2.save()
        self.assertEqual(2, Member.objects.all().count())