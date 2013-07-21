#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def make_user(request):
    form = pong_app.forms.UserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            userName = request.POST['user_name']
            new_user = User.objects.create(user_name=userName)
            context = {'form': form,}
            return render(request, 'makes/make_user.html', context)
        else:
            raise(Exception)
            form = pong_app.forms.UserForm()
            return render(request, 'makes/make_user.html', {'form': form,})
    else:
        return render(request, 'makes/make_user.html', {'form': form,})


@login_required
def make_team(request):
    form = pong_app.forms.MakeTeam(request.POST)
    if request.method == 'POST':
        name = request.POST['name']
        captain = request.POST['captain']
        captain = User.objects.get(pk=captain)
        Team.objects.create(name=name,
                            captain=captain)
        context = {'form': form,}
        return render(request, 'makes/make_team.html', {'form': form,})
    else:
        form = pong_app.forms.MakeTeam()
        return render(request, 'makes/make_team.html', {'form': form,})


@login_required
def make_league(request):
    form = pong_app.forms.MakeLeague(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            location = request.POST['location']
            sport = request.POST['sport']
            comissioner = request.POST['comissioner']
            name = request.POST['name']
            new_league = League.objects.create(location=location,
                                               sport=sport,
                                               comissioner=comissioner,
                                               name=name)
            context = {'form': form,}
            return render(request, 'makes/make_league.html', context)
        else:
            form = pong_app.forms.MakeLeague()
            return render(request, 'makes/make_league.html', {'form': form,})
    else:
        return render(request, 'makes/make_league.html', {'form': form,})
