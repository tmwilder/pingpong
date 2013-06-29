#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamPlayer

def test(request):
    context = {}
    print request.user
    return render(request, 'test.html', context)

