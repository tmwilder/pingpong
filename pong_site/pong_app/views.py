#Django imports.
from django.http import HttpResponse
from django.shortcuts import render
from pong_site.pong_app.models import Players, Match, TeamLeague, Team, League, TeamPlayer

def index(request):
	context = {}
	return render(request, 'index.html', context)

def standings(request):
	if request.method == 'POST':
		form = pong_app.forms.StandingsForm(request.POST)
		if form.is_valid():
			league = request.POST['league']
			teamSet = TeamLeague.objects.filter(league__exact=league).order_by('elo')
			listforcontext = []
			for teamins in teamSet:
				listforcontext.append([Team.objects.get(pk=teamins.team).name,teamins.elo])
			#return that shit for rendering
	context = {}
	return render(request, 'standings.html', context)
	
def team_profile(request):
	if request.method == 'POST':
		form = pong_app.forms.TeamForm(request.POST)
		if form.is_valid():
			teamID = request.POST['teamID']
			eloset = TeamLeague.objects.filter(team__exact=teamID).order_by('elo')
			demoinfo = Team.objects.get(pk=teamID)
			#return this shit for rendering
	context = {}
	return render(request, 'team_profile.html', context)

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
    if request.method == 'POST':
		form = pong_app.forms.PlayerForm(request.POST)
		if form.is_valid():
			playerName = request.POST['player_name']
			playerNick = request.POST['player_nick']
			new_player = Players.objects.create(player_name=playerName, player_nick=playerNick)
		
		context = {}
		return render(request, 'make_player.html', context)
	    else:
	        form = pong_app.forms.PlayerForm()
	        return render(request, 'make_player.html', {'form': form,})

def update_player(request):
	context = {}
	return render(request, 'update_player.html', context)

def make_team(request):
    if request.method == 'POST':
        form = pong_app.forms.TeamForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/make_team/')
    else:
        form = pong_app.forms.TeamForm()
    return render(request, 'make_team.html', {'form': form,})
	
def update_team(request, team_id):
    if request.method == 'POST':
        add_player_form = pong_app.forms.AddPlayerToTeamForm(request.POST)
        team_form = pong_app.forms.TeamForm(request.POST)
        if add_player_form.is_valid():
            return HttpResponseRedirect('/update_team/')
        if team_form.is_valid():
        	return HttpResponseRedirect('/update_team/')
    else:
        add_player_form = pong_app.forms.AddPlayerToTeamForm()
        players = pong_app.models.Player.objects.filter("team__exact"=team_id)
        team_form = pong_app.forms.TeamForm()
    return render(request,
                  'update_team.html',
                  {'add_player_form': add_player_form,
                   'players': players,
                   'team_form': name_cap_form})

def enter_result(request):
	if request.method == 'POST':
		form = pong_app.forms.ResultForm(request.POST)
		if form.is_valid():
			team1 = request.POST['team1']
			team2 = request.POST['team2']
			result = request.POST['result']
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
				score_1 = result
				score_2 = 1-result
				new_1 = elo1 + kfactor*(score_1 - expected_1)
				new_2 = elo2 + kfactor*(score_2 - expected_2)
				return round(new_1), round(new_2)
			
			team1newelo, team2newelo = elocalc(elo1, elo2, result)
			
			t1 = TeamLeague.objects.get(team__name__exact=team1,league__exact=league)
			t1.elo = team1newelo
			t1.save()
			
			t2 = TeamLeague.objects.get(team__name__exact=team2,league__exact=league)
			t2.elo = team2newelo
			t2.save()
			
			context = {}
			return render(request, 'enter_result.html', context)
		else:
			form = pong_app.forms.ResultForm()
			
