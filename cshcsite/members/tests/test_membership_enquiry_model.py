import logging
from django.test import TestCase
from ..models import MembershipEnquiry

log = logging.getLogger(__name__)


class MembershipEnquiryTest(TestCase):
    """Tests for the MembershipEnquiry model"""

    def test_membership_enquiries_can_be_added_and_removed(self):
        """ Tests that membership enquiries can be added to the database and then removed """
        countBefore = MembershipEnquiry.objects.all().count()
        enquiry1 = MembershipEnquiry(first_name="Test", last_name="Enquiry 1", email="test@example.com")
        enquiry2 = MembershipEnquiry(first_name="Test", last_name="Enquiry 2", email="test@example.com")
        enquiry1.save()
        enquiry2.save()
        self.assertEqual(countBefore + 2, MembershipEnquiry.objects.all().count())
        enquiry1.delete()
        enquiry2.delete()
        self.assertEqual(countBefore, MembershipEnquiry.objects.all().count())

