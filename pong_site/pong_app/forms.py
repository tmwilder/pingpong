from django import forms
from pong_app.models import Match, TeamLeague, Team, League, TeamUser


class UpdateUserInfo(forms.Form):
    username = forms.CharField(max_length="64", required=False)
    email = forms.CharField(max_length="64", required=False)
    first_name = forms.CharField(max_length="64", required=False)
    last_name = forms.CharField(max_length="64", required=False)
    #TODO move to seperate process.
    password = forms.CharField(max_length="64", required=False)

    def get_exposed_fields(self):
        return ['username', 'email', 'first_name', 'last_name', 'password']


class MakeLeague(forms.Form):
    location = forms.CharField(max_length="64", required=False)
    sport = forms.CharField(max_length="64", required=False)
    name = forms.CharField(max_length="64", required=False)
    commissioner = forms.IntegerField()


class MakeTeam(forms.Form):
    name = forms.CharField(max_length="64", required=False)
    captain = forms.IntegerField()


class UpdateTeamInfo(forms.Form):
    captain = forms.CharField(max_length="64", required=False)
    name = forms.CharField(max_length="64", required=False)

    def get_exposed_fields(self):
        return ['captain', 'name']


class UpdateLeagueInfo(forms.Form):
    location = forms.CharField(max_length="64", required=False)
    sport = forms.CharField(max_length="64", required=False)
    name = forms.CharField(max_length="64", required=False)
    commissioner = forms.CharField(max_length="64", required=False)

    def get_exposed_fields(self):
        return ['location', 'sport', 'name', 'commissioner']


class AddUserToTeam(forms.Form):
    user_id = forms.IntegerField()
    team_id = forms.IntegerField()


class AddTeamToLeague(forms.Form):
    team_id = forms.IntegerField()
    league_id = forms.IntegerField()


class InputResult(forms.Form):

    def __init__(self, league_id, *args, **kwargs):
        super(InputResult, self).__init__(*args, **kwargs)
        team_leagues = TeamLeague.objects.filter(league__exact=league_id).select_related("team__name")
        teams = [(team_league.team.id, team_league.team.name) for team_league in team_leagues]
        self.fields["team1"] = forms.ChoiceField(choices=teams)
        self.fields["team2"] = forms.ChoiceField(choices=teams)

    result = forms.ChoiceField(choices=[(-1, "Team 1 Won"), (0, "Tie"), (1, "Team 2 Won")])
    match_info = forms.CharField(max_length="2000")


def pre_pop(form, model_instance):
    """
    Takes a form instance and a model instance representing one row of data.
    Populates the form with that row's values using the django form initial
    attribute.
    When the form is rendered, the initial field values are set
    using that dict.

    """
    initial_vals = {}
    for field_name in form.get_exposed_fields():
        field_val = getattr(model_instance, field_name)
        initial_vals[field_name] = field_val
    form.initial = initial_vals
    return form