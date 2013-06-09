#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Player, Match, TeamLeague, Team, League, TeamPlayer

def update_player(request):
    context = {}
    return render(request, 'update_player.html', context)

def update_team(request, team_id=1):
    try:
        team_id = int(team_id)
    except ValueError:
        team_id = 1
    #TODO consider default behavior for team_id.
    if request.method == 'POST':
        add_player_form = pong_app.forms.AddPlayerToTeamForm(request.POST)
        team_form = pong_app.forms.TeamForm(request.POST)
        if add_player_form.is_valid():
            return HttpResponseRedirect('/update_team/')
        if team_form.is_valid():
            return HttpResponseRedirect('/update_team/')
        raise(Exception("DEV exception: It looks like we submitted an invalid form. Let's spec better behavior."))
    else:
        add_player_form = pong_app.forms.AddPlayerToTeamForm()
        players = pong_app.models.Player.objects.filter(teamplayer__team_id__exact=team_id).values("player_name")
        team_form = pong_app.forms.TeamForm()
        return render(request,
                      'update_team.html',
                      {'add_player_form': add_player_form,
                       'players': players,
                       'team_form': team_form})

def update_league(request):
    raise(Exception("Not implemented"))
        
        

