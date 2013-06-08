from django.conf.urls import patterns, include, url
import pong_app.views.misc as misc
import pong_app.views.makes as makes
import pong_app.views.profiles as profiles
import pong_app.views.add_x_to_y as add_x_to_y
import pong_app.views.updates as updates

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^index/{0,1}.*$', misc.index),
	url(r'^enter_result/{0,1}.*$', misc.enter_result),
	#Make
	url(r'^make_player/{0,1}.*$', makes.make_player),
	url(r'^make_team/{0,1}.*$', makes.make_team),
	url(r'^make_league/{0,1}.*$', makes.make_league),
    #Update
	url(r'^update_player/{0,1}$', updates.update_player),
    url(r'^update_team/{0,1}$', updates.update_team),
	url(r'^update_team/(?P<team_id>\d+).*$', updates.update_team),
	#Add
	url(r'^add_team_to_league/{0,1}.*$', add_x_to_y.add_team_to_league),
	url(r'^add_player_to_team/{0,1}.*$', add_x_to_y.add_player_to_team),
	#Profiles
	url(r'^team_profile/{0,1}$', profiles.team_profile),
    url(r'^player_profile/{0,1}$', profiles.player_profile),
	url(r'^player_profile/(?P<player_id>\d+).*$', profiles.player_profile),
	url(r'^standings/{0,1}.*$', profiles.standings),
)
