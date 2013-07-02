#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User


def add_user_to_team(request):
    form = pong_app.forms.AddUserToTeamForm(request.POST)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        team_id = request.POST['team_id']
        team = Team.objects.get(pk=user_id)
        user = User.objects.get(pk=team_id)
        new_team_user = TeamUser.objects.create(user=user,
                                                team=team)
        context = {'form': form,}
        return render(request, 'add_user_to_team.html', {'form': form,})
    else:
        form = pong_app.forms.AddUserToTeamForm()
        return render(request, 'add_user_to_team.html', {'form': form,})
        
def add_team_to_league(request):
    form = pong_app.forms.AddTeamToLeagueForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            team_id = request.POST['team_id']
            league_id = request.POST['league_id']
            team_id = Team.objects.get(pk=team_id)
            league_id = League.objects.get(pk=league_id)
            new_team_league = TeamLeague.objects.create(team=team_id, league=league_id)
            context = {'form': form,}
            return render(request, 'add_team_to_league.html', context)
        else:
            form = pong_app.forms.AddTeamToLeagueForm()
            return render(request, 'add_team_to_league.html', {'form': form,})
    else:
        return render(request, 'add_team_to_league.html', {'form': form,})
