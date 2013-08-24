#Django Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
#Our App
import pong_app.forms
import pong_app.decorators as decor
from pong_app.models import TeamLeague, Team, League, TeamUser


def add_user_to_team(request, team_id):
    """
    Internal method that processes a post request to add a user to a team.
    Don't route to this.

    Return a user friendly error message on failure.

    """
    if request.method == 'POST':
        user_name = request.POST['user_name']
        matching_user = User.objects.filter(username__exact=user_name)
        if len(matching_user) == 0:
            return "We couldn't find a user matching the name {0} in our records.".format(user_name)
        user = matching_user[0]
        team = Team.objects.get(pk=team_id)
        if user.id in [team_user.user.id for team_user in TeamUser.objects.filter(team__exact=team_id)]:
            return "User {0} is already on your team!".format(user_name)
        new_team_user = TeamUser.objects.create(user=user,
                                                team=team)
        new_team_user.save()
        return "Added user {0} to your team.".format(user_name)
    else:
        return False


def add_team_to_league(request, league_id):
    form = pong_app.forms.AddTeamToLeague(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            league = League.objects.get(pk=league_id)
            team_name = request.POST['team_name']
            team_captain_name = request.POST['team_captain_name']
            captain_id = User.objects.get(username__exact=team_captain_name).id
            team = Team.objects.filter(name__exact=team_name).filter(captain__exact=captain_id)[0]
            if not decor.verify_user_is_commissioner(request,
                                                     args=(),
                                                     kwargs={"league_id": league.id}):
                return HttpResponseRedirect("/unauthorized")
            new_team_league = TeamLeague.objects.create(team=team, league=league)
            new_team_league.save()
    return render(request, 'add_x_to_y/add_team_to_league.html', {'form': form})
