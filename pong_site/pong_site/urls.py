from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
import pong_app.views.misc as misc
import pong_app.views.makes as makes
import pong_app.views.profiles as profiles
import pong_app.views.add_x_to_y as add_x_to_y
import pong_app.views.updates as updates
import pong_app.views.test as test
import pong_app.views.registration as registration

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^index/{0,1}.*$', misc.index),
	url(r'^enter_result/{0,1}.*$', misc.enter_result),
	#Make
	url(r'^make_user/{0,1}.*$', makes.make_user),
	url(r'^make_team/{0,1}.*$', makes.make_team),
	url(r'^make_league/{0,1}.*$', makes.make_league),
    #Update
	url(r'^update_user/{0,1}$', updates.update_user),
    url(r'^update_team/{0,1}$', updates.update_team),
	url(r'^update_team/(?P<team_id>\d+).*$', updates.update_team),
	#Add
	url(r'^add_team_to_league/{0,1}.*$', add_x_to_y.add_team_to_league),
	url(r'^add_user_to_team/{0,1}.*$', add_x_to_y.add_user_to_team),
	#Profiles
	url(r'^team_profile/{0,1}$', profiles.team_profile),
	url(r'^team_profile/(?P<team_id>\d+)/{0,1}$', profiles.team_profile),
    url(r'^user_profile/{0,1}$', profiles.user_profile),
	url(r'^user_profile/(?P<user_id>\d+).*$', profiles.user_profile),
	url(r'^league_profile/(?P<league_id>\d+)/{0,1}$', profiles.league_profile),
	#Authentication
    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout, {'next_page':'/index/'}),
    (r'^accounts/register/$', registration.register),
	#Test
	url(r'^test/{0,1}.*$', test.test)
)