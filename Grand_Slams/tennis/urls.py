from django.urls import path
from .views import *
from .api import *

# list of urls for the api
urlpatterns = [
    path('', index, name='index'),
    path('api/tournaments/', tournaments, name='tournaments'),
    path('api/players/', players, name='players'),
    path('api/players/by-letter/<str:letter>/', players_by_letter, name='players_by_letter'),
    path('api/years/', years, name='years'),
    path('api/players/most-aces/', players_with_most_aces, name='players_with_most_aces'),
    path('api/countries/most-wins/', countries_with_most_wins, name='countries_with_most_wins'),
    path('api/performance-by-hand/', performance_by_hand, name='performance_by_hand'),
    path('api/manage-player/', manage_player, name='manage_player'),
    path('api/manage-player/<int:player_id>/', manage_player, name='manage_player'),
    path('api/update-player/<int:player_id>/', update_player, name='update_player'),
]

