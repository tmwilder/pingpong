#Django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#Our app
import pong_app.forms
from pong_app.models import Team, League


@login_required
def make_user(request):
    form = pong_app.forms.UserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            userName = request.POST['user_name']
            new_user = User.objects.create(user_name=userName)
            new_user.save()
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
    context = {}
    if request.method == 'POST':
        name = request.POST['name']
        user_id = int(User.objects.get(username__exact=request.user.username).id)
        captain = User.objects.get(pk=user_id)
        if len(Team.objects.filter(name__exact=name)) == 0:
            new_team = Team.objects.create(name=name,
                                           captain=captain)
            new_team.save()
            context["make_team_msg"] = "You're now the captain of a team named {0}!".format(name)
        else:
            context["make_team_msg"] = "Someone already snagged the team name {0}!".format(name)
        context['form'] = form
        return render(request, 'makes/make_team.html', context)
    else:
        context['form'] = pong_app.forms.MakeTeam()
        return render(request, 'makes/make_team.html', context)


@login_required
def make_league(request):
    context = {}
    if request.method == 'POST':
        form = pong_app.forms.MakeLeague(request.POST)
        if form.is_valid():
            location = request.POST['location']
            sport = request.POST['sport']
            user = User.objects.get(username__exact=request.user.username)
            name = request.POST['name']
            if len(League.objects.filter(name__exact=name)) == 0:
                new_league = League.objects.create(location=location,
                                                   sport=sport,
                                                   commissioner=user,
                                                   name=name)
                new_league.save()
                context["make_league_msg"] = "You're now the commissioner of a league named {0}!".format(name)
            else:
                context["make_league_msg"] = "Someone already snagged the league name {0}!".format(name)
            context['form'] = form
            return render(request, 'makes/make_league.html', context)
    form = pong_app.forms.MakeLeague()
    return render(request, 'makes/make_league.html', {'form': form,})
