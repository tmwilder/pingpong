#Django imports.
import pong_app.forms
from django.http import HttpResponse
from django.shortcuts import render
from pong_app.models import Player, Match, TeamLeague, Team, League, TeamPlayer

def index(request):
    context = {}
    return render(request, 'index.html', context)

def enter_result(request):
    form = pong_app.forms.ResultForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            team1 = request.POST['team1']
            team2 = request.POST['team2']
            result = request.POST['result']
            league = request.POST['league']
            match_info = request.POST['match_info']
            team1 = Team.objects.get(pk=team1)
            team2 = Team.objects.get(pk=team2)
            league = League.objects.get(pk=league)
            
            #assuming team+league = composite primary key
            team1elo = TeamLeague.objects.get(team=team1,league=league).elo
            team2elo = TeamLeague.objects.get(team=team2,league=league).elo  #does this return ints or strings or what?
            
            #temporary elo recalculation function
            def elocalc(elo1, elo2, result):
                result = (int(result) + 1)/2.0
                elo1 = float(elo1)
                elo2 = float(elo2)
                result = float(result)
                base_elo = 1500  #use this when creating a new teamleague object - i.e. when you add a new team, give it a default elo
                elo_spread = 400
                kfactor = 20
                expected_1 = 1/(1+10**((elo2-elo1)/elo_spread))
                expected_2 = 1/(1+10**((elo1-elo2)/elo_spread))
                score_1 = result
                score_2 = 1-result
                new_1 = elo1 + kfactor*(score_1 - expected_1)
                new_2 = elo2 + kfactor*(score_2 - expected_2)
                return round(new_1), round(new_2)
            
            team1newelo, team2newelo = elocalc(team1elo, team2elo, result)
            
            t1 = TeamLeague.objects.get(team=team1,league=league)
            t1.elo = team1newelo
            t1.save()
            
            t2 = TeamLeague.objects.get(team=team2,league=league)
            t2.elo = team2newelo
            t2.save()

            new_match = Match.objects.create(team1=team1, team2=team2,result=result, start_elo1=team1elo, start_elo2=team2elo,league=league,match_info=match_info)

            form = pong_app.forms.ResultForm()
            context = {'form':form,}
            return render(request, 'enter_result.html', context)

        else:
            form = pong_app.forms.ResultForm()
            return render(request, 'enter_result.html', {'form': form,})
    else:
        form = pong_app.forms.ResultForm()
        return render(request, 'enter_result.html', {'form': form,})
