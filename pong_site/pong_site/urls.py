from django.conf.urls import patterns, include, url
import pong_app.views as pv

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^index/{0,1}.*$', pv.index),
	url(r'^standings/{0,1}.*$', pv.standings),
	url(r'^enter_result/{0,1}.*$', pv.enter_result),
	url(r'^make_player/{0,1}.*$', pv.make_player),
	url(r'^update_player/{0,1}.*$', pv.update_player),
	url(r'^make_team/{0,1}.*$', pv.make_team),
    url(r'^update_team/{0,1}.*$', pv.update_team),
	url(r'^update_team/{0,1}(?P<team_id>\d*).*$', pv.update_team),
	url(r'^team_profile/{0,1}.*$', pv.team_profile),
	url(r'^player_profile/{0,1}.*$', pv.player_profile),
	url(r'^make_league/{0,1}.*$', pv.make_league),
	url(r'^add_team_to_league/{0,1}.*$', pv.add_team_to_league),
	url(r'^add_player_to_team/{0,1}.*$', pv.add_player_to_team),
)
