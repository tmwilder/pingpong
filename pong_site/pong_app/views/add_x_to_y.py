#Django
from django.contrib.auth.models import User
#Our App
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
    if request.method == 'POST':
        team_name = request.POST['team_name']
        matching_team = Team.objects.filter(name__exact=team_name)
        if len(matching_team) == 0:
            return "We couldn't find a team matching the name {0} in our records.".format(team_name)
        team = matching_team[0]
        league = League.objects.get(pk=league_id)
        if team.id in [team_league.team.id for team_league in TeamLeague.objects.filter(league__exact=league_id)]:
            return "Team {0} is already in your league!".format(team_name)
        new_team_league = TeamLeague.objects.create(league=league,
                                                    team=team)
        new_team_league.save()
        return "Added team {0} to your league.".format(team_name)
    else:
        return False
