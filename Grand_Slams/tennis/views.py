from django.shortcuts import render
from .models import *

# it retrieves the data from all the models and it renders them on the index.html template
def index(request):
    tournaments = Tournament.objects.all()
    players = Players.objects.all()
    matches = Matches.objects.all()
    match_stats = MatchStats.objects.all()
    player_matches = PlayerMatch.objects.all()
    countries = Country.objects.all()
    hands = Hand.objects.all()
    
    context = {
        'tournaments': tournaments,
        'players': players,
        'matches': matches,
        'match_stats': match_stats,
        'player_matches': player_matches,
        'countries': countries,
        'hands': hands
    }
    
    return render(request, 'index.html', context)