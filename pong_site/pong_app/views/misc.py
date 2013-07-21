#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User
from django.db.models import Q #Django object to do logic in filtering.
from django.contrib.auth.decorators import login_required


def unauthorized(request):
    context = {}
    return render(request, 'misc/unauthorized.html', context)


@login_required
def index(request):
    """Development page to make it faster to navigate the site while prototyping."""
    context = {}
    return render(request, 'misc/index.html', context)


@login_required
def enter_result(request):
    form = pong_app.forms.InputResult(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            team1 = request.POST['team1']
            team2 = request.POST['team2']
            result = request.POST['result']
            league = request.POST['league']
            match_info = request.POST['match_info']
            team1 = Team.objects.get(pk=team1)
            team2 = Team.objects.get(pk=team2)
            league = League.objects.get(pk=league)

            #assuming team+league = composite primary key
            team1elo = TeamLeague.objects.get(team=team1, league=league).elo
            team2elo = TeamLeague.objects.get(team=team2, league=league).elo  #does this return ints or strings or what?

            team1newelo, team2newelo = _elocalc(team1elo, team2elo, result)

            t1 = TeamLeague.objects.get(team=team1, league=league)
            t1.elo = team1newelo
            t1.save()

            t2 = TeamLeague.objects.get(team=team2, league=league)
            t2.elo = team2newelo
            t2.save()

            new_match = Match.objects.create(team1=team1,
                                             team2=team2,
                                             result=result,
                                             start_elo1=team1elo,
                                             start_elo2=team2elo,
                                             league=league,
                                             match_info=match_info)

            form = pong_app.forms.InputResult()
            context = {'form':form,}
            return render(request, 'misc/enter_result.html', context)

        else:
            form = pong_app.forms.InputResult()
            return render(request, 'misc/enter_result.html', {'form': form,})
    else:
        form = pong_app.forms.InputResult()
        return render(request, 'misc/enter_result.html', {'form': form,})


@login_required
def team_matches(request, team_id):
    """
    Shows all matches for one team.
    Left to only this functionality rather than more powerful search based on YAGNI.

    """
    matches = Match.objects.filter(Q(team1__exact=team_id) | Q(team2__exact=team_id)).select_related()
    return render(request, 'misc/team_matches.html', { 'matches': matches })


@login_required
def leagues(request):
    leagues = League.objects.all()
    return render(request, 'misc/leagues.html', { 'leagues': leagues })


@login_required
def teams(request):
    teams = Team.objects.all()
    return render(request, 'misc/teams.html', { 'teams': teams })


def _elocalc(elo1, elo2, result):
    """
    Calculates elo for the two teams after a match is finished.

    Result is -1, 0, or 1 to indicate team 2 wins, tie, team 1 wins
    respectively.

    """
    result = (int(result) + 1)/2.0
    elo1 = float(elo1)
    elo2 = float(elo2)
    result = float(result)
    base_elo = 1500  #use this when creating a new teamleague object - i.e. when you add a new team, give it a default elo
    elo_spread = 400
    kfactor = 20
    expected_1 = 1/(1+10**((elo2-elo1)/elo_spread))
    expected_2 = 1/(1+10**((elo1-elo2)/elo_spread))
    score_1 = result
    score_2 = 1-result
    new_1 = elo1 + kfactor*(score_1 - expected_1)
    new_2 = elo2 + kfactor*(score_2 - expected_2)
    return round(new_1), round(new_2)