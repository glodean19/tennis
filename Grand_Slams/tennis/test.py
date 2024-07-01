import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from .model_factories import *
from .serializers import *

'''
Some reference: https://github.com/erkarl/django-rest-framework-oauth2-provider-example/blob/master/apps/users/tests.py
'''
# testing PlayerSerializer
class PlayersSerializerTest(APITestCase):

    # data to test
    def setUp(self):
        self.hand_L = HandFactory(hand='L', hand_description='Left')
        self.hand_R = HandFactory(hand='R', hand_description='Right')
        self.country = CountryFactory(ioc='FIN', country_name='Finland')

        self.player = PlayersFactory(
            player_name='Player 1',
            hand=self.hand_L,
            height=180,
            ioc=self.country
        )
        self.serializer = PlayerSerializer(instance=self.player)

    # test to verify if the serializer contains the expected fields
    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = ['player_name', 'height', 'hand', 'ioc']

        # Ensure expected fields are in the serialized data
        for field in expected_fields:
            self.assertIn(field, data)

        # Ensure write_only fields are not in the serialized data
        write_only_fields = ['country_name', 'hand_description']
        for field in write_only_fields:
            self.assertNotIn(field, data)

    # test to create a player
    def test_create_player(self):
        data = {
            'player_name': 'Player 2',
            'height': 175,
            'hand_description': 'Right',
            'country_name': 'Canada',
        }
        serializer = PlayerSerializer(data=data)
        # verifies that the serializer is valid and the player is created with the correct data
        self.assertTrue(serializer.is_valid())
        player = serializer.save()
        self.assertEqual(player.player_name, data['player_name'])
        self.assertEqual(player.height, data['height'])
        self.assertEqual(player.hand.hand_description, data['hand_description'])
        self.assertEqual(player.ioc.country_name, data['country_name'])

    # test to update an existing player
    def test_update_player(self):
        data = {
            'player_name': 'Updated Player Name',
            'height': 185,
            'hand_description': 'Right',
            'country_name': 'Canada',
        }
        # partial = True for partial updates
        serializer = PlayerSerializer(instance=self.player, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        player = serializer.save()
        self.assertEqual(player.player_name, data['player_name'])
        self.assertEqual(player.height, data['height'])
        self.assertEqual(player.hand.hand_description, data['hand_description'])
        self.assertEqual(player.ioc.country_name, data['country_name'])


class TournamentTest(APITestCase):
    def setUp(self):
        self.tournament1 = TournamentFactory()
        self.tournament2 = TournamentFactory()

    # test to retrieve the list of tournaments
    def test_retrieve_tournament(self):
        url = reverse('tournaments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # test to retrieve the year of the tournaments
    def test_list_tournaments_by_year(self):
        url = reverse('years')  
        response = self.client.get(url, {'year': 2017})  
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlayersTest(APITestCase):
    # data needed for the test
    def setUp(self):
        self.hand_L = HandFactory(hand='L', hand_description='Left')
        self.country = CountryFactory(ioc='HAI', country_name='Haiti')
        self.player1 = PlayersFactory(hand=self.hand_L, ioc=self.country)

    # test retrieving the list of players
    def test_retrieve_player(self):
        url = reverse('players') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test listing players by the letter of their name
    def test_list_players_by_letter(self):
        url = reverse('players_by_letter', kwargs={'letter': 'A'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test creating a new player
    def test_manage_player_create(self):
        data = {
            'fullname': 'New Player',
            'country': 'Germany',
            'height': 180,
            'hand': 'Right',
        }
        url = reverse('manage_player') 
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Players.objects.count(), 2) 

    # test updating an existing player
    def test_manage_player_update(self):
        data = {
            'player_name': 'Updated Player Name',
            'height': 190,
            'player_id': self.player1.player_id,
        }
        url = reverse('update_player', kwargs={'player_id': self.player1.player_id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.player1.refresh_from_db()
        self.assertEqual(self.player1.player_name, 'Updated Player Name')
        self.assertEqual(self.player1.height, 190)

    # test deleting an existing player
    def test_manage_player_delete(self):
        url = reverse('manage_player', kwargs={'player_id': self.player1.player_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Players.objects.filter(player_id=self.player1.player_id).exists())

class MatchStatsTest(APITestCase):

    def setUp(self):
        self.match = MatchesFactory()
        self.match_stats1 = MatchStatsFactory(match_id=self.match)
        self.match_stats2 = MatchStatsFactory(match_id=self.match)

    # test to check if the endpoint is available
    def test_players_with_most_aces(self):
        url = reverse('players_with_most_aces')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# this class contains tests to check if the endpoints are available 
class PlayerMatchTest(APITestCase):

    def setUp(self):
        self.player_match1 = PlayerMatchFactory()
        self.player_match2 = PlayerMatchFactory()
    
    def test_countries_with_most_wins(self):
        url = reverse('countries_with_most_wins') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_performance_by_hand(self):
        url = reverse('performance_by_hand')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
