#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Player, Match, TeamLeague, Team, League, TeamPlayer

def standings(request):
    if request.method == 'POST':
        form = pong_app.forms.StandingsForm(request.POST)
        if form.is_valid():
            league = request.POST['league']
            teamSet = TeamLeague.objects.filter(league=league).order_by('-elo')
            listforcontext = []
            for teamins in teamSet:
                listforcontext.append([teamins.team.name,teamins.elo])
            context = {'query_results':listforcontext}
            return render(request, 'standings.html', context)
    else:
        form = pong_app.forms.StandingsForm()
        context = {'form':form,}
        return render(request, 'standings.html', context)

def team_profile(request):
    if request.method == 'POST':
        form = pong_app.forms.TeamProfileForm(request.POST)
        if form.is_valid():
            team = request.POST['team']
            team1 = Team.objects.get(pk=team)
            teamleaguelist = TeamLeague.objects.filter(team=team)
            context = {'team':team1, 'teamleague':teamleaguelist}
            return render(request, 'team_profile.html', context)
        else:
            form = pong_app.forms.TeamProfileForm()
            context = {'form':form,}
            return render(request, 'team_profile.html', context)
    else:
        form = pong_app.forms.TeamProfileForm()
        context = {'form':form,}
        return render(request, 'team_profile.html', context)

def player_profile(request, player_id=0): #TODO refactor this monstrosity of a view.
    try:
        player_id=int(player_id)
    except ValueError:
        player_id=1 #TODO fix to required arg once index.html is improved.
    team_players = TeamPlayer.objects.filter(player__exact=player_id)
    team_leagues = [TeamLeague.objects.filter(team__exact=team_player.team) \
                   for team_player in team_players]
    final_team_leagues = []
    #Aggregate league info.
    for team_league_set in team_leagues:
        for team_league in team_league_set:
            final_team_leagues.append(team_league)
    team_names = [team_player.team.name for player in team_players]
    team_elos = [team_league.elo for team_league in final_team_leagues]
    name_elos = zip(team_names, team_elos)
    #Get the player.
    player = Player.objects.get(pk=player_id)
    context = {"player": player,
               "name_elos": name_elos}
    return render(request, 'player_profile.html', context)

