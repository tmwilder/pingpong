#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User


def league_profile(request, league_id):
    team_set = TeamLeague.objects.filter(league=league_id).order_by('-elo')
    #TODO swap from ID to passing in the team name.
    context = {'team_leagues': team_set}
    return render(request, 'league_standings.html', context)


def team_profile(request, team_id):
    team_users = TeamUser.objects.filter(team__exact=team_id).select_related('user__id', 'user__username')
    team_leagues = TeamLeague.objects.filter(team__exact=team_id).select_related('elo', 'league__sport', 'league__elo', 'league__name', 'league__id')
    context = { 'team_users': team_users,
                'team_leagues': team_leagues }
    return render(request,  'team_profile.html', context)

def user_profile(request, user_id):
    """
    1. A record for each team elo that team has.
    2. Links through these records to each team and league for the user.

    """
    team_leagues = []
    team_users = TeamUser.objects.filter(id__exact=user_id).all()
    name_and_ids = { team_user.team.name: team_user.team.id for team_user in team_users }
    for team_name, team_id in name_and_ids.items():
        team_league_dicts = TeamLeague.objects.filter(team__exact=team_id).values("id", "elo")
        for team_league in team_league_dicts:
            league = League.objects.get(pk=team_league["id"])
            team_leagues.append({"team_name": team_name,
                                 "team_id": team_id,
                                 "elo": team_league["elo"],
                                 "league_name": league.name,
                                 "league_id": league.id,
                                 "league_sport": league.sport})
    context = {'team_leagues': team_leagues}
    return render(request, 'user_profile.html', context)   

