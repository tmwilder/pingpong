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
    team_form = pong_app.forms.pre_pop(form=team_form, model_instance=team)
    #Return page info regardless.
    context = {'team_users': team_users, 'team_form': team_form, 'team': team}
    return render(request, 'update_team.html', context)


@login_required #TODO finish/debug
def update_league(request, league_id):
    league = League.objects.get(pk=league_id)
    if request.method == 'POST':
        team_to_drop = request.POST.get('team_to_drop')
        if team_to_drop is not None:
            TeamLeague.objects.filter("team__exact"=team_to_drop).filter("league__exact"=league_id).delete()
        league_form = pong_app.forms.UpdateLeagueInfo(request.POST)
        if league_form.is_valid():
            for key, value in team_form.cleaned_data.items():
                setattr(league, key, value)
            league.save()
    else:
        league_form = pong_app.forms.UpdateLeagueInfo()
    league_form = pong_app.forms.pre_pop(form=league_form, model_instance=league)
    context = {'league': league, 'league_form': league_form}
    return rendeR(request, "update_league.html", context)