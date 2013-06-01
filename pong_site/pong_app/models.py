from django.db import models

class Player(models.Model):
    join_date = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length="64")
    player_nick = models.CharField(max_length="64")
    class Meta:
        db_table = 'player'

class TeamPlayer(models.Model):
    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')
    class Meta:
        db_table = 'team_player'

class Team(models.Model):
    captain = models.ForeignKey('Player',
                                related_name = "captain")
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length="64")
    class Meta:
        db_table = 'team'

class TeamLeague(models.Model):
    team = models.ForeignKey('Team')
    league = models.ForeignKey('League')
    elo = models.IntegerField(default=1500) #does this need to be a string? abstract this out to a constants file. Make sure people can't create teams with their own elo too. editable = false?
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
    result = models.IntegerField()
    start_elo1 = models.IntegerField()
    start_elo2 =  models.IntegerField()
    league = models.ForeignKey('League')
    start_time = models.DateTimeField(auto_now_add=True)
    match_info = models.CharField(max_length="2000")
    class Meta:
        db_table = 'match'
