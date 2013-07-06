#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def update_user(request, user_id):
    context = {}
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
    return render(request, 'update_team.html', {'team_users': team_users, 'team_form': team_form, 'team': team})


@login_required
def update_league(request, league_id):
    raise(Exception("Not implemented"))



