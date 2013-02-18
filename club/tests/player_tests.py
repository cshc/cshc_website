from django.test import TestCase
from django.db import IntegrityError
from club.models import Player
from club.models.choices import PlayerGender, PlayerPosition

class PlayerTest(TestCase):

    def setUp(self):
        self.test_player = Player(first_name="Graham", surname="McCulloch", gender=PlayerGender.MALE, pref_position=PlayerPosition.FORWARD)
        
    def test_players_can_be_added_and_removed(self):
        """ Tests that players can be added to the database and then removed """
        player1 = Player(first_name="Graham", surname="McCulloch", gender=PlayerGender.MALE, pref_position=PlayerPosition.FORWARD)
        player2 = Player(first_name="Mark", surname="Williams", gender=PlayerGender.MALE, pref_position=PlayerPosition.MIDFIELDER)
        player1.save()
        player2.save()
        self.assertEqual(2, Player.objects.all().count())
        player1.delete()
        player2.delete()
        self.assertEqual(0, Player.objects.all().count())

    def test_player_first_name_and_surname_must_be_specified(self):
        """ Tests that you must specify the first name and surname of the player """
        player_with_no_first_name = Player(surname="McCulloch", gender=PlayerGender.MALE, pref_position=PlayerPosition.FORWARD)
        self.assertEqual(None, player_with_no_first_name.first_name)
        self.assertRaisesMessage(IntegrityError, "club_player.first_name may not be NULL", player_with_no_first_name.save)
        player_with_no_surname = Player(first_name="Graham", gender=PlayerGender.MALE, pref_position=PlayerPosition.FORWARD)
        self.assertEqual(None, player_with_no_surname.surname)
        self.assertRaisesMessage(IntegrityError, "club_player.surname may not be NULL", player_with_no_surname.save)


    def test_multiple_players_can_have_the_same_first_name_and_surname(self):
        """ 
        Tests that its possible to have multiple players with the same first name and surname. 
        Note that this may make it very hard to select the right player!

        """
        player1 = Player(first_name="Graham", surname="McCulloch", gender=PlayerGender.MALE, pref_position=PlayerPosition.FORWARD)
        player2 = Player(first_name=player1.first_name, surname=player1.surname, gender=PlayerGender.MALE, pref_position=PlayerPosition.MIDFIELDER)
        player1.save()
        player2.save()
        self.assertEqual(2, Player.objects.all().count())