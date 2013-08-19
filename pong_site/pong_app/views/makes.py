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
    if request.method == 'POST':
        name = request.POST['name']
        user_id = int(User.objects.get(username__exact=request.user.username).id)
        captain = User.objects.get(pk=user_id)
        new_team = Team.objects.create(name=name,
                                       captain=captain)
        new_team.save()
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
            user = User.objects.get(username__exact=request.user.username)
            name = request.POST['name']
            new_league = League.objects.create(location=location,
                                               sport=sport,
                                               commissioner=user,
                                               name=name)
            new_league.save()
            context = {'form': form,}
            return render(request, 'makes/make_league.html', context)
        else:
            form = pong_app.forms.MakeLeague()
            return render(request, 'makes/make_league.html', {'form': form,})
    else:
        return render(request, 'makes/make_league.html', {'form': form,})
