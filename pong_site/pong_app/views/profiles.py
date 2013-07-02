#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User

def league_standings(request, league_id):
    team_set = TeamLeague.objects.filter(league=league_id).order_by('-elo')
    #TODO swap from ID to passing in the team name.
    context = {'team_leagues': team_set}
    return render(request, 'league_standings.html', context)

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

def user_profile(request, user_id=0): #TODO refactor this monstrosity of a view.
    try:
        user_id=int(user_id)
    except ValueError:
        user_id=1 #TODO fix to required arg once index.html is improved.
    team_users = TeamUser.objects.filter(user__exact=user_id)
    team_leagues = [TeamLeague.objects.filter(team__exact=team_user.team) \
                   for team_user in team_users]
    final_team_leagues = []
    #Aggregate league info.
    for team_league_set in team_leagues:
        for team_league in team_league_set:
            final_team_leagues.append(team_league)
    team_names = [team_user.team.name for user in team_users]
    team_elos = [team_league.elo for team_league in final_team_leagues]
    name_elos = zip(team_names, team_elos)
    #Get the user.
    user = User.objects.get(pk=user_id)
    context = {"user": user,
               "name_elos": name_elos}
    return render(request, 'user_profile.html', context)

