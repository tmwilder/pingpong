from django import forms


class UpdateUserInfo(forms.Form):
    user_name = forms.CharField(max_length="64")
    email = forms.CharField(max_length="64")
    first_name = forms.CharField(max_length="64")
    last_name = forms.CharField(max_length="64")
    #TODO move to seperate process.
    password = forms.CharField(max_length="64")

    
class UpdateTeamInfo(forms.Form):
    captain = forms.CharField(max_length="64")
    name = forms.CharField(max_length="64")


class UpdateLeagueInfo(forms.Form):
    location = forms.CharField(max_length="64")
    sport = forms.CharField(max_length="64")
    name = forms.CharField(max_length="64")
    comissioner = forms.CharField(max_length="64")


class AddUserToTeam(forms.Form):
    user_id = forms.IntegerField()
    team_id = forms.IntegerField()


class AddTeamToLeague(forms.Form):
    team_id = forms.IntegerField()
    league_id = forms.IntegerField()


class InputResult(forms.Form):
    team1 = forms.IntegerField()
    team2 = forms.IntegerField()
    result = forms.IntegerField()
    league = forms.IntegerField()
    match_info = forms.CharField(max_length="2000")