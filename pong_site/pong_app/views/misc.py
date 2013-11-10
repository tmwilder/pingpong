#Standard library
import datetime
#Django imports
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League
from django.db.models import Q #Django object to do logic in filtering.
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#Our app
import pong_app.forms


def unauthorized(request):
    context = {}
    return render(request, 'misc/unauthorized.html', context)


def about(request):
    context = {}
    return render(request, 'misc/about.html', context)


@login_required
def index(request):
    """Development page to make it faster to navigate the site while prototyping."""
    context = {}
    return render(request, 'misc/index.html', context)


@login_required
def enter_result(request, league_id):
    league = League.objects.get(pk=league_id)
    form = pong_app.forms.InputResult(data=request.POST, league_id=league_id)
    context = {}
    if request.method == 'POST':
        team1 = request.POST['team1']
        team2 = request.POST['team2']
        result = request.POST['result']
        match_info = request.POST['match_info']
        start_time = request.POST['start_time']
        team1 = Team.objects.get(pk=team1)
        team2 = Team.objects.get(pk=team2)
        league = League.objects.get(pk=league_id)

        #assuming team+league = composite primary key
        if team1 != team2:
            team1elo = TeamLeague.objects.get(team=team1, league=league).elo
            team2elo = TeamLeague.objects.get(team=team2, league=league).elo

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
                                             match_info=match_info,
                                             start_time=start_time)
            new_match.save()
            context["result_msg"] = "Succesfully entered match result."
        else:
            context["result_msg"] = "A team cannot play iteself! Please enter different teams."

    form = pong_app.forms.InputResult(league_id=league_id)
    context['form'] = form
    context['league'] = league
    return render(request, 'misc/enter_result.html', context)


@login_required
def team_league_matches(request, team_id, league_id):
    """
    Shows all matches for one team.
    Left to only this functionality rather than more powerful search based on YAGNI.

    """
    matches = Match.objects.filter(Q(team1__exact=team_id) | Q(team2__exact=team_id)).filter(league__exact=league_id).select_related()
    team = Team.objects.get(pk=team_id)
    league = League.objects.get(pk=league_id)
    elos = []
    for match in matches:
        if match.team1.id == int(team_id):
            elo = match.start_elo1
        elif match.team2.id == int(team_id):
            elo = match.start_elo2
        elos.append({"start_time": match.start_time, "start_elo": elo} )
    return render(request, 'misc/team_league_matches.html', {'matches': matches,
                                                             'team': team,
                                                             'league': league,
                                                             'elos': elos})


@login_required
def leagues(request):
    find_league_form = pong_app.forms.FindLeagueForm(request.POST)
    if request.method == 'POST':
        if find_league_form.is_valid():
            team_name = request.POST["league_name"]
            leagues = League.objects.filter(name__contains=team_name)
        else:
            leagues = League.objects.all()    
    else:
        leagues = League.objects.all()
    context = {
        "leagues": leagues,
        "find_league_form": find_league_form
    }
    return render(request, 'misc/leagues.html', context)


@login_required
def teams(request):
    find_team_form = pong_app.forms.FindTeamForm(request.POST)
    if request.method == 'POST':
        if find_team_form.is_valid():
            team_name = request.POST["team_name"]
            teams = Team.objects.filter(name__contains=team_name)
        else:
            teams = Team.objects.all()    
    else:
        teams = Team.objects.all()
    context = {
        "teams": teams,
        "find_team_form": find_team_form
    }
    return render(request, 'misc/teams.html', context)


def _elocalc(elo1, elo2, result):
    """
    Calculates elo for the two teams after a match is finished.

    Result is -1, 0, or 1 to indicate team 2 wins, a tie, or team 1 wins
    respectively.

    """
    result = (int(result) + 1)/2.0
    elo1 = float(elo1)
    elo2 = float(elo2)
    result = float(result)
    elo_spread = 400
    kfactor = 20
    expected_1 = 1/(1+10**((elo2-elo1)/elo_spread))
    expected_2 = 1/(1+10**((elo1-elo2)/elo_spread))
    score_1 = result
    score_2 = 1-result
    new_1 = elo1 + kfactor*(score_1 - expected_1)
    new_2 = elo2 + kfactor*(score_2 - expected_2)
    return round(new_1), round(new_2)
