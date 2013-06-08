#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Player, Match, TeamLeague, Team, League, TeamPlayer

def make_player(request):
    form = pong_app.forms.PlayerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            playerName = request.POST['player_name']
            playerNick = request.POST['player_nick']
            new_player = Player.objects.create(player_name=playerName,
                                               player_nick=playerNick)
            context = {'form': form,}
            return render(request, 'make_player.html', context)
        else:
            raise(Exception)
            form = pong_app.forms.PlayerForm()
            return render(request, 'make_player.html', {'form': form,})
    else:
        return render(request, 'make_player.html', {'form': form,})

def make_team(request):
    form = pong_app.forms.TeamForm(request.POST)
    if request.method == 'POST':
        team_name = request.POST['team_name']
        team_captain = request.POST['team_captain']
        captain = Player.objects.get(pk=team_captain)
        Team.objects.create(name=team_name,
                            captain=captain)
        context = {'form': form,}
        return render(request, 'make_team.html', {'form': form,})
    else:
        form = pong_app.forms.TeamForm()
        return render(request, 'make_team.html', {'form': form,})

def make_league(request):    
    form = pong_app.forms.LeagueForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            location = request.POST['location']
            sport = request.POST['sport']
            new_league = League.objects.create(location=location, sport=sport)
            context = {'form': form,}
            return render(request, 'make_league.html', context)
        else:
            form = pong_app.forms.LeagueForm()
            return render(request, 'make_league.html', {'form': form,})
    else:
        return render(request, 'make_league.html', {'form': form,})
