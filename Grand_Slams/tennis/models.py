'''
Some reference: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
'''

from django.db import models

# define the tournament table in the database and its fields
class Tournament(models.Model):
    tourney_id = models.CharField(max_length=50, primary_key=True)
    tourney_name = models.CharField(max_length=100, null=False)
    surface = models.CharField(max_length=20, null=True)
    draw_size = models.IntegerField(null=True)
    tourney_level = models.CharField(max_length=10, null=True)
    tourney_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.tourney_name} ({self.tourney_date})"
    
    # specify the table name in the database
    class Meta:
        db_table = 'tennis_tournament'

# define the hand table in the database and its fields 
class Hand(models.Model):
    hand = models.CharField(max_length=1, primary_key=True)
    hand_description = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.hand_description
    
    # specify the table name in the database
    class Meta:
        db_table = 'tennis_hand'

# define the country table in the database and its fields   
class Country(models.Model):
    ioc = models.CharField(max_length=3, primary_key=True)
    country_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.country_name
    
    # specify the table name in the database
    class Meta:
        db_table = 'tennis_country'

# define the players table in the database and its fields
class Players(models.Model):
    player_id = models.IntegerField(primary_key=True)
    player_name = models.CharField(max_length=100, null=False)
    hand = models.ForeignKey(Hand, on_delete=models.CASCADE, null=True)
    height = models.IntegerField(null=True)
    ioc = models.ForeignKey(Country, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.player_name} ({self.ioc})"
    
    # specify the table name in the database
    class Meta:
        db_table = 'tennis_players'

# define the matches table in the database and its fields
class Matches(models.Model):
    match_id = models.CharField(max_length=100, primary_key=True)
    tourney_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match_num = models.IntegerField(null=True)
    score = models.CharField(max_length=50, null=True)
    best_of = models.CharField(max_length=5, null=True)
    round = models.CharField(max_length=10, null=True)
    minutes = models.IntegerField(null=True)

    def __str__(self):
        return f"Match {self.match_id} in {self.tourney_id.tourney_name}"
    
    # specify the table name in the database
    class Meta:
        db_table = 'tennis_matches'

# define the matchstats table in the database and its fields
class MatchStats(models.Model):
    match_stats_id = models.CharField(max_length=100, primary_key=True)
    match_id = models.ForeignKey(Matches, on_delete=models.CASCADE)
    ace = models.IntegerField(null=True)
    df = models.IntegerField(null=True)
    svpt = models.IntegerField(null=True)
    firstIn = models.IntegerField(null=True)
    firstWon = models.IntegerField(null=True)
    secondWon = models.IntegerField(null=True)
    SvGms = models.IntegerField(null=True)
    bpSaved = models.IntegerField(null=True)
    bpFaced = models.IntegerField(null=True)

    def __str__(self):
        return f"MatchStats ID: {self.match_stats_id}, Match ID: {self.match_id.match_id}"
    
    # specify the table name in the database
    class Meta:
        db_table = 'tennis_matchstats'

# define the playermatch table in the database and its fields
class PlayerMatch(models.Model):
    player_id = models.ForeignKey(Players, on_delete=models.CASCADE)
    match_id = models.ForeignKey(Matches, on_delete=models.CASCADE)
    player_role = models.CharField(max_length=10, null=True)
    seed = models.IntegerField(null=True)
    entry = models.CharField(max_length=10, null=True)
    ranking = models.IntegerField(null=True)
    ranking_points = models.IntegerField(null=True)
    age = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.player_id.player_name} in match {self.match_id.match_id}"
    
    # specify the table name in the database
    class Meta:
        db_table = 'tennis_playermatch'