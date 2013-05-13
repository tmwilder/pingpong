from django.http import HttpResponse
from django.shortcuts import render
from pong_site.pong_app.models import Players

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
