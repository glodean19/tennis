'''
Some reference: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site
This file customise the Django admin interface with the tennis app models and fields. 
Created superuser 'admin' with password 'pass-admin' to access the interface. Used to check
the result of the post quest.
'''

from django.contrib import admin
from .models import *

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('tourney_id', 
                    'tourney_name', 
                    'surface', 
                    'draw_size', 
                    'tourney_level', 
                    'tourney_date') 


class PlayersAdmin(admin.ModelAdmin):
    list_display = ('player_id', 
                    'player_name', 
                    'hand', 
                    'height', 
                    'ioc')



class MatchesAdmin(admin.ModelAdmin):
    list_display = ('match_id', 
                    'tourney_id', 
                    'match_num', 
                    'score', 
                    'best_of', 
                    'round', 
                    'minutes')


class MatchStatsAdmin(admin.ModelAdmin):
   list_display = ('match_stats_id',
                   'match_id', 
                   'ace', 
                   'df', 
                   'svpt', 
                   'firstIn', 
                   'firstWon', 
                   'secondWon', 
                   'SvGms', 
                   'bpSaved', 
                   'bpFaced')


class PlayerMatchAdmin(admin.ModelAdmin):
   list_display = ('player_id', 
                   'match_id', 
                   'player_role', 
                   'seed', 
                   'entry', 
                   'ranking', 
                   'ranking_points', 
                   'age') 


class CountryAdmin(admin.ModelAdmin):
   list_display = ('ioc', 
                   'country_name') 


class HandAdmin(admin.ModelAdmin):
    list_display = ('hand', 
                    'hand_description') 


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Matches, MatchesAdmin)
admin.site.register(MatchStats, MatchStatsAdmin)
admin.site.register(PlayerMatch, PlayerMatchAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Hand, HandAdmin)

