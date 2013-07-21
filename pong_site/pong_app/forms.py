from django import forms


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
    team1 = forms.IntegerField()
    team2 = forms.IntegerField()
    result = forms.IntegerField()
    league = forms.IntegerField()
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