#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User

def make_user(request):
    form = pong_app.forms.UserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            userName = request.POST['user_name']
            new_user = User.objects.create(user_name=userName)
            context = {'form': form,}
            return render(request, 'make_user.html', context)
        else:
            raise(Exception)
            form = pong_app.forms.UserForm()
            return render(request, 'make_user.html', {'form': form,})
    else:
        return render(request, 'make_user.html', {'form': form,})

def make_team(request):
    form = pong_app.forms.TeamForm(request.POST)
    if request.method == 'POST':
        team_name = request.POST['team_name']
        team_captain = request.POST['team_captain']
        captain = User.objects.get(pk=team_captain)
        Team.objects.create(name=team_name,
                            captain=captain)
        context = {'form': form,}
        return render(request, 'make_team.html', {'form': form,})
    else:
        form = pong_app.forms.TeamForm()
        return render(request, 'make_team.html', {'form': form,})

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
