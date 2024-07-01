from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Case, When, IntegerField
from django.db.models.functions import Left
from .models import *
from .serializers import *

# get request to return the tournament's names without duplicates
#similar to SELECT DISTINCT in SQL
@api_view(['GET'])
def tournaments(request):
    data = list(Tournament.objects.values('tourney_name').distinct())
    return Response(data)

'''
players and players_by_letter GET requests work together in showing the list of players selected by letters
'''
# this GET request iterates through all trhe letters in the alphabet, including Z (+ 1) and it returns the numbers of 
# recors who's name is starting with each letter of the alphabet in JSON format
@api_view(['GET'])
def players(request):
    letters = []
    for letter in range(ord('A'), ord('Z') + 1):
        letters.append({'letter': chr(letter), 'count': Players.objects.filter(player_name__startswith=chr(letter)).count()})
    return Response(letters)

# it retrieves a list of names starting with the selected letter, calling the PlayerSerialzer or displaying a message if any players are found
# PlayerSerializer used to convert the model instance 'players' in dictionaries.
@api_view(['GET'])
def players_by_letter(request, letter):
    players = Players.objects.filter(player_name__startswith=letter.upper())
    if not players.exists():
        return Response({'message': f"There aren't any players with names starting with the letter {letter.upper()}"})
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)

# GET request to retrieve the tournament's years without duplicates.
@api_view(['GET'])
def years(request):
    data = list(Tournament.objects.annotate(year=Left('tourney_date', 4)).values('year').distinct().order_by('year'))
    return Response(data)


# Some Reference: https://stackoverflow.com/questions/68557002/using-djangos-case-when-queryset-conditions-to-set-more-than-one-value
# https://forum.djangoproject.com/t/using-case-when-value-with-annotate-on-related-object/15355
# in this GET request, the total number of aces are returned only when the conditions of the player role in the PlayerMatch and 
# the match_stats_id ending with the corresponding letter (w for winner and l for loser) are met. This ensure that for each match, 
#only aces of the same player (either for matches won or lost) are summed.
@api_view(['GET'])
def players_with_most_aces(request):
    players = Players.objects.annotate(
        total_aces=Sum(
            Case(
                When(
                    playermatch__player_role='winner',
                    playermatch__match_id__matchstats__match_stats_id__endswith='-w',
                    then='playermatch__match_id__matchstats__ace'
                ),
                When(
                    playermatch__player_role='loser',
                    playermatch__match_id__matchstats__match_stats_id__endswith='-l',
                    then='playermatch__match_id__matchstats__ace'
                ),
                output_field=IntegerField(),
                default=0
            )
        )
    ).values('player_name', 'total_aces').order_by('-total_aces')[:10]
    return Response(players)

# For each match won, it's counted 1 and later added to get the total number of matched won by country
@api_view(['GET'])
def countries_with_most_wins(request):
    countries = PlayerMatch.objects.select_related('player_id__ioc').values(
        'player_id__ioc__country_name').annotate(
        wins=Sum(Case(When(player_role='winner', then=1), output_field=IntegerField()))
    ).order_by('-wins')[:10]
    return Response(countries)

# similar to the previous GET request, it counts 1 for each match won or lost. It returns
# the number of matches won and lost associated to the dominant hand reported in the dataset
@api_view(['GET'])
def performance_by_hand(request):
    hand_performance = PlayerMatch.objects.select_related('player_id__hand').values(
        'player_id__hand__hand_description').annotate(
        wins=Sum(Case(When(player_role='winner', then=1), output_field=IntegerField())),
        losses=Sum(Case(When(player_role='loser', then=1), output_field=IntegerField())))
    return Response(hand_performance)

# Some reference: https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
# the POST requet retrieves the data inputted in the form by the user. Player data are passed
# to the PlayerSerializer, where after checking if the data are valid based on the models, 
# they are saved in the databse. If the method is DELETE, after retrieving the player object based on the 
# player_id, it deletes the player record from the database, returning status 204
@api_view(['POST', 'DELETE'])
def manage_player(request, player_id=None):
    if request.method == 'POST':
        # Add player logic
        player_name = request.data.get('fullname')
        country_name = request.data.get('country')
        height = request.data.get('height')
        hand_description = request.data.get('hand')

        # Prepare player data
        player_data = {
            'player_name': player_name,
            'country_name': country_name,
            'height': height,
            'hand_description': hand_description
        }

        # Validate the player data
        player_serializer = PlayerSerializer(data=player_data)
        if not player_serializer.is_valid():
            return Response({'error': player_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        player_instance = player_serializer.save()

        # Prepare response data with newly created player details
        response_data = {
            'player': player_serializer.data,
        }

        response_data['player']['player_id'] = player_instance.player_id  
        # Returns 201 Created response and a success message
        return Response({'status': 'success', 'message': 'Player added successfully', 'data': response_data}, status=status.HTTP_201_CREATED)
    
    
    # if the method is DELETE
    elif request.method == 'DELETE':
        try:
            # it fetches the player with the given player_id. If the player exists, it deletes the record and returns a 204 No Content response
            player = Players.objects.get(player_id=player_id)
            player.delete()
            return Response({'status': 'success', 'message': 'Player deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        # If the player doesn't exist, it returns a not found response. any other error has a 500 Internal Server Error response
        except Players.DoesNotExist:
            return Response({'status': 'error', 'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # this error when the request is not POST or DELETE
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Some reference: https://medium.com/@sinturana250/django-post-put-get-delete-requests-example-rest-apis-chapter-19-c449b6260b2a
# https://djangogrpcframework.readthedocs.io/en/latest/patterns/partial_update.html
# It uses the PUT and PATCH methods to update a player. The serializer is set to pass not all the fields for partial updates
@api_view(['PUT', 'PATCH'])
def update_player(request, player_id):
    try:
        player = Players.objects.get(player_id=player_id)
    except Players.DoesNotExist:
        return Response({'status': 'error', 'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)
    # partial argument allows partial updates
    serializer = PlayerSerializer(player, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'message': 'Player updated successfully', 'data': serializer.data})
    else:
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
