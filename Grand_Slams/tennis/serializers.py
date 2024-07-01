'''
Some refrence: https://stribny.name/blog/drf-different-request-response-serializers/
https://www.django-rest-framework.org/tutorial/1-serialization/
https://www.geeksforgeeks.org/serializers-django-rest-framework/
'''

from rest_framework import serializers
from .models import Players, Hand, Country
'''
write-only: country_name and hand_description are not part of the Players model itself 
but are used to create or update Country and Hand instances. 
They are included in the input data as ioc and hand but are excluded from the serialized output 
because they are not direct attributes of the Players model.
read-only: ioc and hand are derived from the related models Country and Hand. 
They are included in the serialized output but are not part of the input data 
because they are managed through the related instances as country_name and hand_description.
'''
class PlayerSerializer(serializers.ModelSerializer):
    # these fields are not stored in the Players table
    country_name = serializers.CharField(write_only=True)
    hand_description = serializers.CharField(write_only=True)
    # these are derived from country and hand tables
    ioc = serializers.CharField(required=False)
    hand = serializers.CharField(required=False)

    # includes specific fields
    class Meta:
        model = Players
        fields = ['player_name', 'height', 'hand', 'ioc', 'country_name', 'hand_description']

    def create(self, validated_data):
        hand_description = validated_data.pop('hand_description')
        country_name = validated_data.pop('country_name')
        # it finds the last player in the database and increments their player_id by 1.
        # if no players exist, starts with player_id = 1.
        last_player = Players.objects.all().order_by('player_id').last()
        if last_player:
            player_id = last_player.player_id + 1
        else:
            player_id = 1  

        validated_data['player_id'] = player_id
        # it uses the first letter of the description as the key. 
        hand, _ = Hand.objects.get_or_create(hand=hand_description[:1].upper(),
                                           defaults={'hand_description': hand_description})
        # it uses the first three letters of the name as the key.
        country, _ = Country.objects.get_or_create(ioc=country_name[:3].upper(),
                                                   defaults={'country_name': country_name})

        validated_data['hand'] = hand
        validated_data['ioc'] = country

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # to update hand and country
        hand_description = validated_data.pop('hand_description', None)
        country_name = validated_data.pop('country_name', None)
        # If the hand_description is provided, finds or creates the corresponding Hand instance and updates the player's hand
        if hand_description:
            hand, _ = Hand.objects.get_or_create(hand=hand_description[:1].upper(),
                                                 defaults={'hand_description': hand_description})
            instance.hand = hand
        # If the country_name is provided, finds or creates the corresponding Country instance and updates the player's ioc
        if country_name:
            country, _ = Country.objects.get_or_create(ioc=country_name[:3].upper(),
                                                       defaults={'country_name': country_name})
            instance.ioc = country
        # it updates player_name and height with the new values
        instance.player_name = validated_data.get('player_name', instance.player_name)
        instance.height = validated_data.get('height', instance.height)
        instance.save()
        return instance


