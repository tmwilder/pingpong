#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Player, Match, TeamLeague, Team, League, TeamPlayer

def add_player_to_team(request):
    form = pong_app.forms.AddPlayerToTeamForm(request.POST)
    if request.method == 'POST':
        player_id = request.POST['player_id']
        team_id = request.POST['team_id']
        team = Team.objects.get(pk=player_id)
        player = Player.objects.get(pk=team_id)
        new_team_player = TeamPlayer.objects.create(player=player,
                                                    team=team)
        context = {'form': form,}
        return render(request, 'add_player_to_team.html', {'form': form,})
    else:
        form = pong_app.forms.AddPlayerToTeamForm()
        return render(request, 'add_player_to_team.html', {'form': form,})
        
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
