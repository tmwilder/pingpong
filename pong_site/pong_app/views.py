from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	context = {}
	return render(request, 'index.html', context)

def standings(request):
	context = {}
	return render(request, 'standings.html', context)

def enter_result(request):
	context = {}
	return render(request, 'enter_result.html', context)

def make_player(request):
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
