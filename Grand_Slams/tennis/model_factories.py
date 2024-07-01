import factory
from django.test import TestCase
from .models import *

# factory classes to create the each model instances
# Sequence: unique values in a specific format
# Faker: realistic, random values
# SubFactory: associations with another factory
class TournamentFactory(factory.django.DjangoModelFactory):
    tourney_id = factory.Sequence(lambda n: f"Tournament_{n}")
    tourney_name = factory.Faker('company')
    surface = factory.Faker('word')
    draw_size = factory.Faker('random_int', min=16, max=128, step=16)
    tourney_level = factory.Faker('random_element', elements=('ATP', 'WTA'))
    tourney_date = factory.Faker('date')
    
    class Meta:
        model =Tournament


class HandFactory(factory.django.DjangoModelFactory):
    hand = factory.Sequence(lambda n: f"hand{n}")
    hand_description = factory.Faker('word')

    class Meta:
        model = Hand

 
  
class CountryFactory(factory.django.DjangoModelFactory):
    ioc = factory.Sequence(lambda n: f"IOC{n}")
    country_name = factory.Faker('word')
    
    class Meta:
        model = Country


class PlayersFactory(factory.django.DjangoModelFactory):
    player_id = factory.Sequence(lambda n: n)
    player_name = factory.Faker('name')
    hand = factory.SubFactory(HandFactory) 
    height = factory.Faker('random_int', min=160, max=210)
    ioc = factory.SubFactory(CountryFactory) 
 
    class Meta:
        model = Players


class MatchesFactory(factory.django.DjangoModelFactory):
    match_id = factory.Sequence(lambda n: f"Match_{n}")
    tourney_id = factory.SubFactory(TournamentFactory)
    match_num = factory.Sequence(lambda n: n)
    score = factory.Faker('numerify', text='###-###')
    best_of = '3'
    round = factory.Faker('word')
    minutes = factory.Faker('random_int', min=60, max=240)
    
    class Meta:
        model = Matches


class MatchStatsFactory(factory.django.DjangoModelFactory):
    match_stats_id = factory.Sequence(lambda n: f"Stats_{n}")
    match_id = factory.SubFactory(MatchesFactory)
    ace = factory.Faker('random_int', min=0, max=20)
    df = factory.Faker('random_int', min=0, max=10)
    svpt = factory.Faker('random_int', min=10, max=100)
    firstIn = factory.Faker('random_int', min=5, max=50)
    firstWon = factory.Faker('random_int', min=3, max=25)
    secondWon = factory.Faker('random_int', min=2, max=20)
    SvGms = factory.Faker('random_int', min=1, max=10)
    bpSaved = factory.Faker('random_int', min=0, max=5)
    bpFaced = factory.Faker('random_int', min=0, max=5)
    
    class Meta:
        model = MatchStats


class PlayerMatchFactory(factory.django.DjangoModelFactory):
    player_id = factory.SubFactory(PlayersFactory)
    match_id = factory.SubFactory(MatchesFactory)
    player_role = factory.Faker('random_element', elements=('Player', 'Opponent'))
    seed = factory.Faker('random_int', min=1, max=32)
    entry = factory.Faker('random_element', elements=('WC', 'Q', 'LL'))
    ranking = factory.Faker('random_int', min=1, max=100)
    ranking_points = factory.Faker('random_int', min=10, max=2000)
    age = factory.Faker('random_int', min=18, max=40)
    
    class Meta:
        model = PlayerMatch