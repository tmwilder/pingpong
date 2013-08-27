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
    context = {}
    team_users = TeamUser.objects.filter(team__exact=team_id).select_related("user__name", "user__id")
    team = Team.objects.get(pk=team_id)
    if request.method == 'POST':
        #Delete a user if one was specified to be dropped.
        user_to_drop = request.POST.get("user_to_drop")
        if user_to_drop is not None:
            team_user = TeamUser.objects.filter(user__exact=user_to_drop, team__exact=team_id)[0]
            context['drop_user_msg'] = "Removed user {0} from your team!".format(team_user.user.username)
            team_user.delete()

        team_form = pong_app.forms.UpdateTeamInfo(request.POST)
        if team_form.is_valid(): #TODO swap to email + name or something user facing to identify captain.
            team_row = Team.objects.get(pk=team_id)
            name = team_form.cleaned_data['name']
            if name not in ['', team_row.name]:
                if len(Team.objects.filter(name__exact=name)) == 0:
                    team_row.name = name
                    team_row.save()
                    context["change_name_msg"] = "You've changed team name to {0}!".format(name)
                else:
                    context["change_name_msg"] = "Someone else already grabbed the name {0}!".format(name)

        user_form = pong_app.forms.AddUserToTeam(request.POST)
        if user_form.is_valid():
            user_status = add_x_to_y.add_user_to_team(request, team_id)
            if type(user_status) is str:
                context['add_user_msg'] = user_status
    else:
        #When no form was submitted.
        team_form = pong_app.forms.UpdateTeamInfo()
    user_form = pong_app.forms.AddUserToTeam()
    team_form = pong_app.forms.pre_pop(form=team_form, model_instance=team)
    #Return page info regardless.
    context['team_users'] = team_users
    context['team_form'] = team_form
    context['add_user_form'] = user_form
    context['team'] = team
    return render(request, 'updates/update_team.html', context)


@login_required #TODO finish/debug
@decor.user_passes_test_request(decor.verify_user_is_commissioner)
def update_league(request, league_id):
    context = {}
    league = League.objects.get(pk=league_id)
    context['league'] = league
    if request.method == 'POST':
        team_to_drop = request.POST.get('team_to_drop')
        if team_to_drop is not None:
            team_league = TeamLeague.objects.filter(team__exact=team_to_drop).filter(league__exact=league_id)[0]
            context['drop_team_msg'] = "Dropped team {0} from your league!".format(team_league.team.name)
            team_league.delete()

        league_form = pong_app.forms.UpdateLeagueInfo(request.POST)
        if league_form.is_valid():
            update_items = \
                {'commissioner_name': league_form.cleaned_data["commissioner"],
                 'name': league_form.cleaned_data["name"],
                 'sport': league_form.cleaned_data["sport"],
                 'location': league_form.cleaned_data["location"]}
            update = False
            for item_name, item_val in update_items.items():
                if item_name != "commissioner_name":
                    old_val = getattr(league, item_name)
                    if item_val not in [old_val, '']:
                        update = True
                        setattr(league, item_name, item_val)
                else:
                    old_comm = getattr(league, 'commissioner')
                    if item_val != '':
                        commissioner = User.objects.filter(username__exact=update_items['commissioner_name'])[0]
                        if commissioner.id != old_comm:
                            league.commissioner = commissioner
                            update = True

            if update is True:
                league.save()
                context['update_league_msg'] = "Updated league info."

        add_team_form = pong_app.forms.AddTeamToLeague(request.POST)
        if add_team_form.is_valid():
            team_status = add_x_to_y.add_team_to_league(request, league_id)
            if type(team_status) is str:
                context['add_team_msg'] = team_status

    else:
        league_form = pong_app.forms.UpdateLeagueInfo()
        add_team_form = pong_app.forms.AddTeamToLeague()
    team_leagues = TeamLeague.objects.filter(league=league_id).select_related('elo', 'team__id', 'team__name').order_by('-elo')
    league_form = pong_app.forms.pre_pop(form=league_form, model_instance=league)
    context['league_form'] = league_form
    context['team_leagues'] = team_leagues
    context['add_team_to_league_form'] = add_team_form
    return render(request, "updates/update_league.html", context)