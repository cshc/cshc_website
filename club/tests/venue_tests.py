from django.test import TestCase
from django.db import IntegrityError
from club.models import Venue
from club.models.choices import *

class VenueTest(TestCase):

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_phone = "01223 123456"
        self.test_addr1 = "Apartment A"
        self.test_addr2 = "123 Some Street"
        self.test_addr3 = "Some District"
        self.test_city = "Cambridge"
        self.test_postcode = "CB1 1AA"
        self.test_notes = "Some notes about the venue"

    def test_venues_can_be_added_and_removed(self):
        """ Tests that venues can be added to the database and then removed """
        venue1 = Venue(name="Venue 1", short_name="Ven1", url=self.test_url, phone=self.test_phone, 
                       addr1=self.test_addr1, addr2=self.test_addr2, addr3=self.test_addr3, addr_city=self.test_city, addr_postcode=self.test_postcode, 
                       notes=self.test_notes)
        venue2 = Venue(name="Venue 2", short_name="Ven2", url=self.test_url, phone=self.test_phone, 
                       addr1=self.test_addr1, addr2=self.test_addr2, addr3=self.test_addr3, addr_city=self.test_city, addr_postcode=self.test_postcode, 
                       notes=self.test_notes)
        venue1.save()
        venue2.save()
        self.assertEqual(2, Venue.objects.all().count())
        venue1.delete()
        venue2.delete()
        self.assertEqual(0, Venue.objects.all().count())

    def test_both_venue_name_and_short_name_must_be_supplied(self):
        """ Tests that you must specify both the name and short name of the venue """
        venue_with_no_name = Venue(short_name="Ven1", url=self.test_url, phone=self.test_phone, 
                                   addr1=self.test_addr1, addr2=self.test_addr2, addr3=self.test_addr3, addr_city=self.test_city, addr_postcode=self.test_postcode, 
                                   notes=self.test_notes)
        self.assertEqual(None,venue_with_no_name.name)
        self.assertRaisesMessage(IntegrityError, "club_venue.name may not be NULL", venue_with_no_name.save)

        venue_with_no_short_name = Venue(name="Venue 1", url=self.test_url, phone=self.test_phone, 
                                   addr1=self.test_addr1, addr2=self.test_addr2, addr3=self.test_addr3, addr_city=self.test_city, addr_postcode=self.test_postcode, 
                                   notes=self.test_notes)
        self.assertEqual(None,venue_with_no_short_name.short_name)
        self.assertRaisesMessage(IntegrityError, "club_venue.short_name may not be NULL", venue_with_no_short_name.save)

    def test_only_venue_name_and_short_name_need_to_be_supplied(self):
        """Tests that all other Venue fields are optional"""
        basic_venue = Venue(name="My Venue", short_name="MyVen")
        basic_venue.save()
        self.assertEqual(1, Venue.objects.all().count())

    def test_venue_names_must_be_unique(self):
        """Tests that two venues with the same name cannot be added"""
        venue1 = Venue(name="My venue", short_name="MyVen")
        venue2 = Venue(name=venue1.name, short_name="MyOtherVen")
        venue1.save()
        self.assertRaises(IntegrityError, venue2.save)
