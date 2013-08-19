#Django imports.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
#Our app
import pong_app.forms
import pong_app.views.add_x_to_y as add_x_to_y
import pong_app.decorators as decor
from pong_app.models import Match, TeamLeague, Team, League, TeamUser


@login_required
@decor.user_passes_test_request(decor.verify_user_id_in_url)
def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        user_form = pong_app.forms.UpdateUserInfo(request.POST)
        if user_form.is_valid():
            fields_to_change = request.POST.items()
            #Are we evil for using txxhis private method?
            user_fields = user_form.get_exposed_fields()
            for key, value in fields_to_change:
                if key in user_fields and key != '':
                    setattr(user, key, value)
            user.save()
    else:
        user_form = pong_app.forms.UpdateUserInfo()
    user_form = pong_app.forms.pre_pop(form=user_form, model_instance=user)
    context = {'user': user, 'user_form': user_form}
    return render(request, 'updates/update_user.html', context)


@login_required
@decor.user_passes_test_request(decor.verify_user_is_captain)
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
            team_row.name = name
            team_row.save()

        user_form = pong_app.forms.AddUserToTeam(request.POST)
        if user_form.is_valid():
            user_success = add_x_to_y.add_user_to_team(request, team_id)
            if user_success == "unauthorized":
                return HttpResponseRedirect("/unauthorized")
    else:
        #When no form was submitted.
        team_form = pong_app.forms.UpdateTeamInfo()
    user_form = pong_app.forms.AddUserToTeam()
    team_form = pong_app.forms.pre_pop(form=team_form, model_instance=team)
    #Return page info regardless.
    context = {'team_users': team_users, 'team_form': team_form, 'add_user_form': user_form, 'team': team}
    return render(request, 'updates/update_team.html', context)


@login_required #TODO finish/debug
@decor.user_passes_test_request(decor.verify_user_is_commissioner)
def update_league(request, league_id):
    league = League.objects.get(pk=league_id)
    add_team_to_league_form = pong_app.forms.AddTeamToLeague()
    if request.method == 'POST':
        team_to_drop = request.POST.get('team_to_drop')
        if team_to_drop is not None:
            TeamLeague.objects.filter(team__exact=team_to_drop).filter(league__exact=league_id).delete()
        league_form = pong_app.forms.UpdateLeagueInfo(request.POST)
        if league_form.is_valid():
            commissioner_id = league_form.cleaned_data["commissioner"]
            if commissioner_id:
                commissioner = User.objects.get(pk=commissioner_id)
                league.commissioner = commissioner
            league.name = league_form.cleaned_data["name"]
            league.sport = league_form.cleaned_data["sport"]
            league.location = league_form.cleaned_data["location"]
            league.save()
        add_x_to_y.add_team_to_league(request, league.id)
    else:
        league_form = pong_app.forms.UpdateLeagueInfo()
    team_leagues = TeamLeague.objects.filter(league=league_id).select_related('elo', 'team__id', 'team__name').order_by('-elo')
    league_form = pong_app.forms.pre_pop(form=league_form, model_instance=league)
    context = {'league': league,
               'league_form': league_form,
               'team_leagues': team_leagues,
               'add_team_to_league_form': add_team_to_league_form}
    return render(request, "updates/update_league.html", context)