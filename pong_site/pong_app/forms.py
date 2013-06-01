from django import forms


class PlayerForm(forms.Form):
    player_name = forms.IntegerField()
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
    
