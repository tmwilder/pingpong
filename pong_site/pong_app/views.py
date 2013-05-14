from django.http import HttpResponse
from django.shortcuts import render
from pong_site.pong_app.models import Players, Match, TeamLeague, Team, League


def index(request):
	context = {}
	return render(request, 'index.html', context)

def standings(request):
	context = {}
	return render(request, 'standings.html', context)
	
def team_profile(request):
	context = {}
	return render(request, 'team_profile.html', context)

def player_profile(request):
	context = {}
	return render(request, 'player_profile.html', context)

def enter_result(request):
	if 'team1' in request.POST:
		team1 = request.POST['team1']
	if 'team2' in request.POST:
		team2 = request.POST['team2']
	if 'result' in request.POST:
		result = request.POST['result']
	if 'league' in request.POST:
		league = request.POST['league']
	
	#assuming team+league = composite primary key
	team1elo = TeamLeague.objects.get(team__name__exact=team1,league__exact=league).elo
	team2elo = TeamLeague.objects.get(team__name__exact=team2,league__exact=league).elo  #does this return ints or strings or what?

	#temporary elo recalculation function
	def elocalc(elo1, elo2, result):
		elo1 = float(elo1)
		elo2 = float(elo2)
		result = float(result)
		base_elo = 1500  #use this when creating a new teamleague object - i.e. when you add a new team, give it a default elo
		elo_spread = 400
		kfactor = 20
		expected_1 = 1/(1+10**((elo2-elo1)/elo_spread))
		expected_2 = 1/(1+10**((elo1-elo2)/elo_spread))
		print expected_1,expected_2
		score_1 = result
		score_2 = 1-result
		new_1 = elo1 + kfactor*(score_1 - expected_1)
		new_2 = elo2 + kfactor*(score_2 - expected_2)
		return new_1, new_2

	team1newelo, team2newelo = elocalc(elo1, elo2, result)
	
	t1 = TeamLeague.objects.get(team__name__exact=team1,league__exact=league)
	t1.elo = team1newelo
	t1.save()

	t2 = TeamLeague.objects.get(team__name__exact=team2,league__exact=league)
	t2.elo = team2newelo
	t2.save()

	context = {}
	return render(request, 'enter_result.html', context)

def make_player(request):
	if 'player_name' in request.POST:
		playerName = request.POST['player_name']
	if 'player_nick' in request.POST:
		playerNick = request.POST['player_nick']

	new_player = Players.objects.create(player_name=playerName, player_nick=playerNick)
	
	context = {}
	return render(request, 'make_player.html', context)

def update_player(request):
	context = {}
	return render(request, 'update_player.html', context)

def make_team(request):
	context = {}
	return render(request, 'make_team.html', context)
	
def update_team(request):
	context = {}
	return render(request, 'update_team.html', context)
