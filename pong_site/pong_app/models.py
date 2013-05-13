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
    class Meta:
        db_table = 'team_players'

class Team(models.Model):
    captain = models.ForeignKey('Team')
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length="64")
    class Meta:
        db_table = 'team'

class TeamLeague(models.Model):
    team = models.ForeignKey('Team')
    league = models.ForeignKey('League')
    elo = models.IntegerField()
    page_rank = models.IntegerField()
    class Meta:
        db_table = 'team_league'

class League(models.Model):
    location = models.CharField(max_length="64")
    sport = models.CharField(max_length="64")
    class Meta:
        db_table = 'league'

class Match(models.Model):
    team1 = models.ForeignKey('Team', related_name="team1")
    team2 = models.ForeignKey('Team', related_name="team2")
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    start_elo1 = models.IntegerField()
    start_elo2 =  models.IntegerField()
    league = models.ForeignKey('League')
    start_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'match'
