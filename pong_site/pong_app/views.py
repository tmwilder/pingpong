#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Player, Match, TeamLeague, Team, League, TeamPlayer

def index(request):
    urls = 	['pong_app.views.index',
	'pong_app.views.standings',
    'pong_app.views.enter_result',
    'pong_app.views.make_player',
    'pong_app.views.update_player',
    'pong_app.views.make_team',
    'pong_app.views.update_team',
    'pong_app.views.team_profile',
    'pong_app.views.player_profile',
    'pong_app.views.make_league',
    'pong_app.views.add_team_to_league',
    'pong_app.views.add_player_to_team']
    nice_names = [path.replace('pong_app.views.', '') for path in urls]
    urls = zip(urls, nice_names)
    context = {'urls': urls}
    return render(request, 'index.html', context)


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
    
def player_profile(request):
    if request.method == 'POST':
        form = pong_app.forms.TeamForm(request.POST)
        if form.is_valid():
            playerID = request.POST['playerID']
            teamset = TeamPlayer.objects.filter(player=playerID)
            teamlist = []
            for teamins in teamset:
                listforcontext.append([Team.objects.get(pk=teamins.team)])
                #think about this shit some more...it's not obvious what's going on here.
    context = {}
    return render(request, 'player_profile', context)

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

def update_player(request):
    context = {}
    return render(request, 'update_player.html', context)


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
    else:
        add_player_form = pong_app.forms.AddPlayerToTeamForm()
        #players = pong_app.models.Player.objects.filter(id__exact=team_id)
        players = pong_app.models.Player.objects.filter(teamplayer__team_id__exact=team_id).values("player_name")
        team_form = pong_app.forms.TeamForm()
    return render(request,
                  'update_team.html',
                  {'add_player_form': add_player_form,
                   'players': players,
                   'team_form': team_form})

def enter_result(request):
    form = pong_app.forms.ResultForm(request.POST)
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
            team1elo = TeamLeague.objects.get(team=team1,league=league).elo
            team2elo = TeamLeague.objects.get(team=team2,league=league).elo  #does this return ints or strings or what?
            
            #temporary elo recalculation function
            def elocalc(elo1, elo2, result):
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
            
            team1newelo, team2newelo = elocalc(team1elo, team2elo, result)
            
            t1 = TeamLeague.objects.get(team=team1,league=league)
            t1.elo = team1newelo
            t1.save()
            
            t2 = TeamLeague.objects.get(team=team2,league=league)
            t2.elo = team2newelo
            t2.save()

            new_match = Match.objects.create(team1=team1, team2=team2,result=result, start_elo1=team1elo, start_elo2=team2elo,league=league,match_info=match_info)

            form = pong_app.forms.ResultForm()
            context = {'form':form,}
            return render(request, 'enter_result.html', context)

        else:
            form = pong_app.forms.ResultForm()
            return render(request, 'enter_result.html', {'form': form,})
    else:
        form = pong_app.forms.ResultForm()
        return render(request, 'enter_result.html', {'form': form,})
            
