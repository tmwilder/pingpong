from django import forms

class StandingsForm(forms.Form):
    league = forms.IntegerField()

class PlayerForm(forms.Form):
    player_name = forms.CharField(max_length="64")
    player_nick = forms.CharField(max_length="64")


class PlayerForm(forms.Form):
    player_name = forms.CharField(max_length="64")
    player_nick = forms.CharField(max_length="64")
    
    
class TeamForm(forms.Form):
    team_captain = forms.CharField(max_length="64")
    team_name = forms.CharField(max_length="64")


class AddPlayerToTeamForm(forms.Form):
    player_name = forms.CharField(max_length="64")


class LeagueForm(forms.Form):
    location = forms.CharField(max_length="64")
    sport = forms.CharField(max_length="64")


class AddTeamToLeagueForm(forms.Form):
    team_id = forms.IntegerField()
    league_id = forms.IntegerField()
    
class ResultForm(forms.Form):
    team1 = forms.IntegerField()
    team2 = forms.IntegerField()
    result = forms.IntegerField()
    league = forms.IntegerField()
    match_info = forms.CharField(max_length="2000")
    
class AddPlayerToTeamForm(forms.Form):
    player_id = forms.IntegerField()
    team_id = forms.IntegerField()
