#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Match, TeamLeague, Team, League, TeamUser
from django.contrib.auth.decorators import login_required


@login_required
def test(request):
    context = {}
    return render(request, 'test.html', context)
