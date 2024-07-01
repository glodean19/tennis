'''
Some reference: https://python.plainenglish.io/importing-csv-data-into-django-models-c92a303623fe
Each script read the csv file located in the data folder and it creates a new object using Django's ORM where each field
correspond to the model's fields. It also uses helper functions for parsing dates and convert NULL or None string values
to python None type values.
'''

import os
import sys
import django
import csv
from datetime import datetime

# Add the project directory to the sys.path
sys.path.append("/home/veronica/Documents/AWD/files/Grand_Slams")
# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Grand_Slams.settings')
# Setup Django
django.setup()

# Import the models after setting up Django
from tennis.models import *

data_folder = '/home/veronica/Documents/AWD/files/Grand_Slams/data'

# Helper function to parse dates
def parse_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d').date()

# Helper function to convert 'NULL' or 'None' strings to python NoneType
def nullify(value):
    if value == 'NULL' or value == 'None' or value == '':
        return None
    return value


# Load Tournament.csv
tournament_file = os.path.join(data_folder, 'Tournament.csv')
with open(tournament_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)  
    for row in csv_reader:
        Tournament.objects.create(
            tourney_id=row[0],
            tourney_name=row[1],
            surface=row[2],
            draw_size=nullify(row[3]),
            tourney_level=row[4],
            tourney_date=parse_date(row[5])
        )

# Load Hand.csv
hand_file = os.path.join(data_folder, 'Hand.csv')
with open(hand_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)  
    for row in csv_reader:
        Hand.objects.create(
            hand=row[0],
            hand_description=row[1]
        )

# Load Country.csv
country_file = os.path.join(data_folder, 'Country.csv')
with open(country_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)  
    for row in csv_reader:
        Country.objects.create(
            ioc=row[0],
            country_name=row[1]
        )

# Load Players.csv
players_file = os.path.join(data_folder, 'Players.csv')
with open(players_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader) 
    for row in csv_reader:
        hand_instance = Hand.objects.get(hand=row[2])
        ioc_instance = Country.objects.get(ioc=row[4])
        Players.objects.create(
            player_id=row[0],
            player_name=row[1],
            hand=hand_instance,
            height=nullify(row[3]),
            ioc=ioc_instance
        )

# Load Matches.csv
matches_file = os.path.join(data_folder, 'Matches.csv')
with open(matches_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        tourney_id = Tournament.objects.get(tourney_id=row[1])
        Matches.objects.create(
            match_id=row[0],
            tourney_id=tourney_id,
            match_num=nullify(row[2]),
            score=nullify(row[3]),
            best_of=nullify(row[4]),
            round=nullify(row[5]),
            minutes=nullify(row[6])
        )


# Load MatchStats.csv
match_stats_file = os.path.join(data_folder, 'Match_Stats.csv')
with open(match_stats_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader) 
    for row in csv_reader:
        match_id = Matches.objects.get(match_id=row[1])
        MatchStats.objects.create(
            match_stats_id = row[0],
            match_id=match_id,
            ace=nullify(row[2]),
            df=nullify(row[3]),
            svpt=nullify(row[4]),
            firstIn=nullify(row[5]),
            firstWon=nullify(row[6]),
            secondWon=nullify(row[7]),
            SvGms=nullify(row[8]),
            bpSaved=nullify(row[9]),
            bpFaced=nullify(row[10])
        )

# Load PlayerMatch.csv
player_match_file = os.path.join(data_folder, 'Player_Match.csv')
with open(player_match_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader) 
    for row in csv_reader:
        player_id = Players.objects.get(player_id=row[0])
        match_id = Matches.objects.get(match_id=row[1])
        PlayerMatch.objects.create(
            player_id=player_id,
            match_id=match_id,
            player_role=nullify(row[2]),
            seed=nullify(row[3]),
            entry=nullify(row[4]),
            ranking=nullify(row[5]),
            ranking_points=nullify(row[6]),
            age=nullify(row[7])
        )


