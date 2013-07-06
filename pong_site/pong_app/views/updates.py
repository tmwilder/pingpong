#Django imports.
import pong_app.forms
from django.http import HttpResponse
import pong_app.decorators as decor
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
@decor.user_passes_test_request(decor.verify_user_id_in_url)
def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        user_form = pong_app.forms.UpdateUserInfo(request.POST)
        if user_form.is_valid():
            fields_to_change = request.POST.items()
            #Are we evil for using this private method?
            user_fields = user_form.get_exposed_fields()
            for key, value in fields_to_change:
                if key in user_fields and key != '':
                    setattr(user, key, value)
            user.save()
    else:
        user_form = pong_app.forms.UpdateUserInfo()
    user_form = pong_app.forms.pre_pop(form=user_form, model_instance=user)
    context = {'user': user, 'user_form': user_form}
    return render(request, 'update_user.html', context)


@login_required
def update_team(request, team_id):
    team_users = TeamUser.objects.filter(team__exact=team_id).select_related("user__name", "user__id")
    team = Team.objects.get(pk=team_id)
    if request.method == 'POST':
        #Delete a user if one was specified to be dropped.
        user_to_drop = request.POST.get("user_to_drop")
        if user_to_drop is not None:
            User.objects.get(pk=user_to_drop).delete()
        team_form = pong_app.forms.UpdateTeamInfo(request.POST)
        if team_form.is_valid():#TODO swap to email + name or something user facing to identify captain.
            team_row = Team.objects.get(pk=team_id)
            name = team_form.cleaned_data['name']
            captain_id = team_form.cleaned_data['captain']
            captain = User.objects.get(pk=captain_id)
            team_row.name = name
            team_row.captain = captain
            team_row.save()
    else:
        #When no form was submitted.
        team_form = pong_app.forms.UpdateTeamInfo()
    #Return page info regardless.
    context = {'team_users': team_users, 'team_form': team_form, 'team': team}
    return render(request, 'update_team.html', context)


@login_required
def update_league(request, league_id):
    raise(Exception("Not implemented"))



