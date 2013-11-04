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
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_PATH}),
    url(r'^index/$', misc.index),
    url(r'^enter_result/(?P<league_id>\d+)/$', misc.enter_result),
    #Make
    url(r'^make_user/$', makes.make_user),
    url(r'^make_team/$', makes.make_team),
    url(r'^make_league/$', makes.make_league),
    #Update
    url(r'^update_user/(?P<user_id>\d+)/$', updates.update_user),
    url(r'^update_team/(?P<team_id>\d+)/$', updates.update_team),
    url(r'^update_league/(?P<league_id>\d+)/$', updates.update_league),
    #Add
    url(r'^add_team_to_league/{0,1}.*$', add_x_to_y.add_team_to_league),
    url(r'^add_user_to_team/{0,1}.*$', add_x_to_y.add_user_to_team),
    #Profiles
    url(r'^team_profile/(?P<team_id>\d+)/$', profiles.team_profile),
    url(r'^user_profile/(?P<user_id>\d+)/$', profiles.user_profile),
    url(r'^league_profile/(?P<league_id>\d+)/$', profiles.league_profile),
    #Authentication
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}),
    url(r'^accounts/register/$', registration.register),
    url(r'^accounts/password_reset/$', registration.password_reset),
    url(r'^accounts/password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>[\d\w-]+)$', registration.password_reset_confirm),
    url(r'^accounts/password_reset_confirm/$', registration.password_reset_confirm),
    url(r'^accounts/password_reset_done/$', registration.password_reset_done),
    url(r'^accounts/password_reset_complete/$', registration.password_reset_complete),
    #Test
    url(r'^test/{0,1}.*$', test.test),
    #Unauthorized
    url(r'^unauthorized.*$', misc.unauthorized),
    #Aggregate pages
    url(r'^team_league_matches/(?P<team_id>\d+)/(?P<league_id>\d+)/$', misc.team_league_matches),
    url(r'^teams/.*$', misc.teams),
    url(r'^leagues/.*$', misc.leagues),
    #Catchall
    url(r'^.*$', redirect.redirectToHome)
)
