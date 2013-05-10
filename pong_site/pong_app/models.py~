from django.db import models

class Players(models.Model):
    team = models.ForeignKey('Team')
    join_date = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length="64")
    player_nick = models.CharField(max_length="64")
    class Meta:
        db_table = 'players'

class TeamPlayers(models.Model):
    team = models.ForeignKey('Team')
    player = models.ForeignKey('Players')
    join_time = models.DateTimeField(auto_now_add=True)
    quit_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'team_players'

class Team(models.Model):
    captain = models.ForeignKey('Team')
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length="64")
    class Meta:
        db_table = 'team'
        
class TeamSport(models.Model):
    team = models.ForeignKey('Team')
    sport = models.ForeignKey('Sport')
    elo = models.IntegerField()
    page_rank = models.IntegerField()
    class Meta:
        db_table = 'team_sport'

class Sport(models.Model):
    location = models.CharField(max_length="64")
    class Meta:
        db_table = 'sports'
    
class Games(models.Model):
    team1 = models.ForeignKey('Team', related_name="team1")
    team2 = models.ForeignKey('Team', related_name="team2")
    match = models.ForeignKey('Match')
    sport = models.ForeignKey('Sport')
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length="64")
    conditions = models.CharField(max_length="64")
    class Meta:
        db_table = 'games'

class Match(models.Model):
    best_of = models.IntegerField()
    class Meta:
        db_table = 'match'
