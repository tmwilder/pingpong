#Standard Library
import os
#Django
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
#Our app
from django.conf import settings
import pong_app.views.misc as misc
import pong_app.views.makes as makes
import pong_app.views.profiles as profiles
import pong_app.views.add_x_to_y as add_x_to_y
import pong_app.views.updates as updates
import pong_app.views.test as test
import pong_app.views.registration as registration
import pong_app.views.redirect as redirect


STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
BASE_URL = settings.BASE_URL

urlpatterns = patterns('',
    #Misc
    url(r'^%s/static/(?P<path>.*)$' % BASE_URL, 'django.views.static.serve', {'document_root': STATIC_PATH}),
    url(r'^%s/{0,1}$' % BASE_URL, redirect.redirectToUserProfile),
    url(r'^%s/index/{0,1}.*$' % BASE_URL, misc.index),
    url(r'^%s/enter_result/(?P<league_id>\d+)/{0,1}$' % BASE_URL, misc.enter_result),
    #Make
    url(r'^%s/make_user/{0,1}.*$' % BASE_URL, makes.make_user),
    url(r'^%s/make_team/{0,1}.*$' % BASE_URL, makes.make_team),
    url(r'^%s/make_league/{0,1}.*$' % BASE_URL, makes.make_league),
    #Update
    url(r'^%s/update_user/(?P<user_id>\d+)/{0,1}$' % BASE_URL, updates.update_user),
    url(r'^%s/update_team/(?P<team_id>\d+)/{0,1}$' % BASE_URL, updates.update_team),
    url(r'^%s/update_league/(?P<league_id>\d+)/{0,1}$' % BASE_URL, updates.update_league),
    #Add
    url(r'^%s/add_team_to_league/{0,1}.*$' % BASE_URL, add_x_to_y.add_team_to_league),
    url(r'^%s/add_user_to_team/{0,1}.*$' % BASE_URL, add_x_to_y.add_user_to_team),
    #Profiles
    url(r'^%s/team_profile/(?P<team_id>\d+)/{0,1}$' % BASE_URL, profiles.team_profile),
    url(r'^%s/user_profile/(?P<user_id>\d+).*$' % BASE_URL, profiles.user_profile),
    url(r'^%s/league_profile/(?P<league_id>\d+)/{0,1}$' % BASE_URL, profiles.league_profile),
    #Authentication
    url(r'^%s/accounts/login/$' % BASE_URL,  login),
    url(r'^%s/accounts/logout/$' % BASE_URL, logout, {'next_page': '/'}),
    url(r'^%s/accounts/register/$' % BASE_URL, registration.register),
    url(r'^%s/accounts/password_reset/$' % BASE_URL, registration.password_reset),
    url(r'^%s/accounts/password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>[\d\w-]+)$' % BASE_URL, registration.password_reset_confirm),
    url(r'^%s/accounts/password_reset_confirm/$' % BASE_URL, registration.password_reset_confirm),
    url(r'^%s/accounts/password_reset_done/$' % BASE_URL, registration.password_reset_done),
    url(r'^%s/accounts/password_reset_complete/$' % BASE_URL, registration.password_reset_complete),
    #Test
    url(r'^%s/test/{0,1}.*$' % BASE_URL, test.test),
    #Unauthorized
    url(r'^%s/unauthorized.*$' % BASE_URL, misc.unauthorized),
    #Aggregate pages
    url(r'^%s/team_league_matches/(?P<team_id>\d+)/(?P<league_id>\d+)/{0,1}.*$'% BASE_URL, misc.team_league_matches),
    url(r'^%s/teams.*$' % BASE_URL, misc.teams),
    url(r'^%s/leagues.*$' % BASE_URL, misc.leagues),
    #Catchall
    url(r'^%s/.*$' % BASE_URL, redirect.redirectToHome)
)
