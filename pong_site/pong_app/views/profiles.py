#Django imports.
import pong_app.forms
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from pong_app.decorators import user_passes_test_request, verify_user_id_in_url
from django.db.models import Q #Django object to do logic in filtering.


@login_required
def league_profile(request, league_id):
    team_set = TeamLeague.objects.filter(league=league_id).select_related('elo', 'team__id', 'team__name').order_by('-elo')
    for index, team in enumerate(team_set):
        team.rank = index + 1
        wins, draws, losses = _get_record(team.id)
        team.wins = wins
        team.draws = draws
        team.losses = losses
    league = League.objects.get(pk=league_id)
    context = {'team_leagues': team_set, 'league': league}
    return render(request, 'profiles/league_profile.html', context)


def _get_record(team_id):
    wins = Match.objects.filter((Q(team1__exact=team_id) & Q(result__exact=1)) | \
                                (Q(team2__exact=team_id) & Q(result__exact=-1))).count()
    draws = Match.objects.filter((Q(team1__exact=team_id) | Q(team2__exact=team_id)) & \
                                  Q(result__exact=0)).count()
    losses = Match.objects.filter((Q(team1__exact=team_id) & Q(result__exact=-1)) | \
                                  (Q(team2__exact=team_id) & Q(result__exact=1))).count()
    return wins, draws, losses


@login_required
def team_profile(request, team_id):
    team = Team.objects.get(pk=team_id)
    team_users = TeamUser.objects.filter(team__exact=team_id).select_related('user__id', 'user__username')
    team_leagues = TeamLeague.objects.filter(team__exact=team_id).select_related('elo', 'league__sport', 'league__elo', 'league__name', 'league__id')
    context = {'team_users': team_users,
               'team_leagues': team_leagues,
               'team': team}
    return render(request,  'profiles/team_profile.html', context)


@login_required
def user_profile(request, user_id):
    """
    1. A record for each team elo that team has.
    2. Links through these records to each team and league for the user.

    """
    team_leagues = []
    team_users = TeamUser.objects.filter(id__exact=user_id).all()
    name_and_ids = {team_user.team.name: team_user.team.id for team_user in team_users}
    for team_name, team_id in name_and_ids.items():
        team_league_dicts = TeamLeague.objects.filter(team__exact=team_id).values("league", "elo")
        for team_league in team_league_dicts:
            league = League.objects.get(pk=team_league["league"])
            team_leagues.append({"team_name": team_name,
                                 "team_id": team_id,
                                 "elo": team_league["elo"],
                                 "league_name": league.name,
                                 "league_id": league.id,
                                 "league_sport": league.sport})
    user = User.objects.get(pk=user_id)
    context = {'target_user': user,
               'team_leagues': team_leagues }
    return render(request, 'profiles/user_profile.html', context)
