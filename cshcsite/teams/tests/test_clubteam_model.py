import logging
from django.test import TestCase
from core.models import TeamGender, TeamOrdinal
from ..models import ClubTeam

log = logging.getLogger(__name__)


class ClubTeamTest(TestCase):
    """Tests for the ClubTeam model"""

    def test_clubteams_can_be_added_and_removed(self):
        """ Tests that club teams can be added to the database and then removed """
        countBefore = ClubTeam.objects.all().count()
        tc1 = ClubTeam(short_name="Test1", long_name="Test team 1", gender=TeamGender.mens, ordinal=TeamOrdinal.T9, position=20)
        tc2 = ClubTeam(short_name="Test2", long_name="Test team 2", gender=TeamGender.ladies, ordinal=TeamOrdinal.T9, position=21)
        tc1.save()
        tc2.save()
        self.assertEqual(countBefore + 2, ClubTeam.objects.all().count())
        tc1.delete()
        tc2.delete()
        self.assertEqual(countBefore, ClubTeam.objects.all().count())
