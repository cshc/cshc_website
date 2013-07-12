import logging
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ..models import Member
from ..views import MemberListView, MemberDetailView

log = logging.getLogger(__name__)


class MemberViewTest(TestCase):
    """Tests for the Member views"""

    def setUp(self):
        self.test_user, u_created = User.objects.get_or_create(username="gm", first_name="Graham", last_name="McCulloch", email="test@test.com")
        self.test_member, m_created = Member.objects.get_or_create(user=self.test_user, gender=Member.GENDER.Male, pref_position=Member.POSITION.Fwd)

    def test_MemberListView(self):
        """ Tests that the MemberListView view contains the test member """
        url = reverse('member_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_member = response.context['member_list'].get(user=self.test_user)
        self.assertMembersEqual(self.test_member, retrieved_member)

    def test_MemberDetailView(self):
        """ Tests that the MemberDetailView view contains the test member """
        url = reverse('member_detail', args=[self.test_member.pk])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_member = response.context['member']
        self.assertMembersEqual(self.test_member, retrieved_member)

    def assertMembersEqual(self, member1, member2):
        self.assertEquals(member1.first_name, member2.first_name)
        self.assertEquals(member1.last_name, member2.last_name)
        self.assertEquals(member1.gender, member2.gender)
        self.assertEquals(member1.pref_position, member2.pref_position)

