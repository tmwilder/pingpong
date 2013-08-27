#Standard library
import itertools
#Django imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q #Django object to do logic in filtering.
#Our app
import pong_app.forms
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from pong_app.decorators import user_passes_test_request, verify_user_id_in_url


@login_required
def league_profile(request, league_id):
    team_league_set = TeamLeague.objects.filter(league__exact=league_id).order_by('-elo')
    for index, team_league in enumerate(team_league_set):
        team_league.rank = index + 1
        wins, draws, losses = _get_record(team_league.team.id, league_id)
        # raise(Exception(team_league.team.id))
        # raise(Exception(repr((wins, draws, losses))))
        setattr(team_league, 'wins', wins)
        setattr(team_league, 'draws', draws)
        setattr(team_league, 'losses', losses)
    league = League.objects.get(pk=league_id)
    context = {'team_leagues': team_league_set, 'league': league}
    return render(request, 'profiles/league_profile.html', context)


def _get_record(team_id, league_id):
    wins = Match.objects.filter((Q(team1__exact=team_id) & Q(result__exact=1)) | \
                                (Q(team2__exact=team_id) & Q(result__exact=-1))).filter(league__exact=league_id).count()
    draws = Match.objects.filter((Q(team1__exact=team_id) | Q(team2__exact=team_id)) & \
                                  Q(result__exact=0)).filter(league__exact=league_id).count()
    losses = Match.objects.filter((Q(team1__exact=team_id) & Q(result__exact=-1)) | \
                                  (Q(team2__exact=team_id) & Q(result__exact=1))).filter(league__exact=league_id).count()
    return wins, draws, losses


@login_required
def team_profile(request, team_id):
    team = Team.objects.get(pk=team_id)
    team_users = TeamUser.objects.filter(team__exact=team_id).select_related('user__id', 'user__username')
    # captain = User.objects.filter(username__exact=request.user.username)
    team_leagues = TeamLeague.objects.filter(team__exact=team_id).select_related('elo', 'league__sport', 'league__elo', 'league__name', 'league__id')
    context = {'team_users': team_users,
               'team_leagues': team_leagues,
               'team': team}
    return render(request, 'profiles/team_profile.html', context)


@login_required
def user_profile(request, user_id):
    """
    1. A record for each team elo that team has.
    2. Links through these records to each team and league for the user.

    """
    team_leagues = []
    teams_without_leagues = []
    team_users = TeamUser.objects.filter(id__exact=user_id).all()
    name_and_ids = {team_user.team.name: team_user.team.id for team_user in team_users}
    for team in Team.objects.filter(captain__exact=user_id):
        name_and_ids[team.name] = team.id
    for team_name, team_id in name_and_ids.items():
        team_league_dicts = TeamLeague.objects.filter(team__exact=team_id).values("league", "elo")
        if team_league_dicts:
            for team_league in team_league_dicts:
                league = League.objects.get(pk=team_league["league"])
                team_leagues.append({"team_name": team_name,
                                     "team_id": team_id,
                                     "elo": team_league["elo"],
                                     "league_name": league.name,
                                     "league_id": league.id,
                                     "league_sport": league.sport})
        else:  #For teams that have not joined a league.
            teams_without_leagues.append({"team_name": team_name,
                                          "team_id": team_id})
    user = User.objects.get(pk=user_id)
    context = {'target_user': user,
               'team_leagues': team_leagues,
               'teams_without_leagues': teams_without_leagues }
    return render(request, 'profiles/user_profile.html', context)
