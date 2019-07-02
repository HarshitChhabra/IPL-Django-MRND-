from django.views import View
from ipl_app.models import *
from django.http import HttpResponse,QueryDict
from django.shortcuts import render,get_object_or_404,redirect
from django.core import serializers
from django.db.models import Sum,Count,Q
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain


distinctTeams = Matches.objects.values('team1','team2').distinct()
teams = []
for team in distinctTeams:
    teams.append(team['team1'])
    teams.append(team['team2'])
teams = list(set(teams))
print(teams)
backgroundColours = {
    'Kings XI Punjab':'#ea2121',
    'Sunrisers Hyderabad':'#f76f0c',
    'Pune Warriors':'#5998c3',
    'Chennai Super Kings':'#ffff00',
    'Gujarat Lions':'#fc7f43',
    'Rising Pune Supergiant':'#be0171',
    'Mumbai Indians':'#3774ab',
    'Rajasthan Royals':'#f7a2cc',
    'Delhi Daredevils':'#272865',
    'Delhi Capitals':'#062889',
    'Kolkata Knight Riders':'#4a2d71',
    'Royal Challengers Bangalore':'#f12f23',
    'Rising Pune Supergiants':'#be0171',
    'Deccan Chargers':'#253d5e',
    'Kochi Tuskers Kerala':'#f48f54'
}

foregroundColours = {
    'Kings XI Punjab':'white',
    'Sunrisers Hyderabad':'white',
    'Pune Warriors':'white',
    'Chennai Super Kings':'black',
    'Gujarat Lions':'white',
    'Rising Pune Supergiant':'white',
    'Mumbai Indians':'white',
    'Rajasthan Royals':'',
    'Delhi Daredevils':'white',
    'Delhi Capitals':'white',
    'Kolkata Knight Riders':'white',
    'Royal Challengers Bangalore':'black',
    'Rising Pune Supergiants':'white',
    'Deccan Chargers':'white',
    'Kochi Tuskers Kerala':'white'
}

class Seasons(View):
    season_list = Season.objects.order_by('-season')
    def get(self,request,*args,**kwargs):
         if kwargs.get('season',-1)!=-1:
             season = Season.objects.get(season=kwargs.get('season'))
             matches = Matches.objects.filter(season=season)
             return HttpResponse(serializers.serialize("json",matches))
         return render(request, template_name='season_details.html',context={'seasons': self.season_list})

class Matches_view(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self,request,*args,**kwargs):
        deliveries = []
        deliveries = Deliveries.objects.filter(match_id=kwargs.get('match_id'))
        print(deliveries)
        # innings = Innings.objects.filter(match_id=kwargs.get('match_id'))
        # for inning in innings:
        #     overs = Overs.objects.filter(inning=inning)
        #     for over in overs:
        #         deliv = Deliveries.objects.filter(over_id = over)
        #         deliveries.append([inning,over,deliv])
        #         #delivExtra = Delivery_Extra_Data.objects.filter()
        #print(deliveries[0].batting_team)
        top3Batsman = Deliveries.objects.filter(match_id=kwargs.get('match_id')).values('batsman','batting_team').annotate(total = Sum('total_runs')).order_by('-total')[:3]
        top3Bowlers = Deliveries.objects.filter(match_id=kwargs.get('match_id')).exclude(player_dismissed = '').values('bowler', 'bowling_team').annotate(count=Count('id')).order_by('-count')[:3]
        extras = Deliveries.objects.filter(match_id=kwargs.get('match_id')).values('batting_team').annotate(extras = Sum('wide_runs')+Sum('bye_runs')+Sum('legbye_runs')+Sum('noball_runs')+Sum('penalty_runs'),total = Sum('total_runs'))
        print(extras)
        #for i in top3Bowlers:
        #    print(i.player_dismissed)

        #print(top3Bowlers)
        return render(request,'match_details.html',context =
            {
                'deliveries':list(deliveries),
                'team1':deliveries[0].batting_team,
                'team2':deliveries[0].bowling_team,
                'top3batsmen':top3Batsman,
                'top3bowlers':top3Bowlers,
                'stats':extras,
                'team1Fore':foregroundColours[deliveries[0].batting_team],
                'team1Back':backgroundColours[deliveries[0].batting_team],
                'team2Fore': foregroundColours[deliveries[0].bowling_team],
                'team2Back': backgroundColours[deliveries[0].bowling_team],
            })

def getPoints(season):
    season = Season.objects.get(season=season)
    matches = Matches.objects.filter(season=season)
    data = dict()
    for match in matches:
        if data.get(match.team1, -1) == -1:
            data[match.team1] = {'played': 0, 'won': 0, 'lost': 0, 'points': 0}
        if data.get(match.team2, -1) == -1:
            data[match.team2] = {'played': 0, 'won': 0, 'lost': 0, 'points': 0}
    for match in matches:
        data[match.team1]['played'] += 1
        data[match.team2]['played'] += 1
        if match.winner == '':
            data[match.team1]['points'] += 1
            data[match.team2]['points'] += 1
        elif match.winner == match.team1:
            data[match.team1]['points'] += 2
            data[match.team1]['won'] += 1
            data[match.team2]['lost'] += 1
        else:
            data[match.team2]['points'] += 2
            data[match.team2]['won'] += 1
            data[match.team1]['lost'] += 1
    queryDict = QueryDict('', mutable=True)
    queryDict.update(data)
    data = dict(sorted(data.items(), key=lambda x: -x[1]['points']))
    return data

class Points(View):
    season_list = Season.objects.order_by('-season')
    def get(self,request,*args,**kwargs):
        if kwargs.get('season',-1) == -1:
            return redirect('/season/'+str(self.season_list[0].season)+'/points/')

        # season = Season.objects.get(season=kwargs.get('season'))
        # matches = Matches.objects.filter(season=season)
        # data = dict()
        # for match in matches:
        #     if data.get(match.team1, -1) == -1:
        #         data[match.team1] = {'played': 0, 'won': 0, 'lost': 0, 'points': 0}
        #     if data.get(match.team2, -1) == -1:
        #         data[match.team2] = {'played': 0, 'won': 0, 'lost': 0, 'points': 0}
        # for match in matches:
        #     data[match.team1]['played'] += 1
        #     data[match.team2]['played'] += 1
        #     if match.winner == '':
        #         data[match.team1]['points'] += 1
        #         data[match.team2]['points'] += 1
        #     elif match.winner == match.team1:
        #         data[match.team1]['points'] += 2
        #         data[match.team1]['won'] += 1
        #         data[match.team2]['lost'] += 1
        #     else:
        #         data[match.team2]['points'] += 2
        #         data[match.team2]['won'] += 1
        #         data[match.team1]['lost'] += 1
        # queryDict = QueryDict('',mutable=True)
        # queryDict.update(data)
        #data = dict(sorted(data.items(),key=lambda x:-x[1]['points']))
        data = getPoints(kwargs.get('season'))
        return render(request,template_name='points.html',context={'data':data,'seasons':self.season_list,'selected_year':kwargs.get('season')})

class Teams(View):
    season_list = Season.objects.order_by('-season')
    def get(self,request,*args,**kwargs):
        if kwargs.get('season',-1) == -1:
            return redirect('/teams/'+str(self.season_list[0].season)+'/')

        season = Season.objects.get(season=kwargs.get('season'))
        teams = Matches.objects.filter(season=season).values('team1').distinct()
        teams = [team['team1'] for team in teams]
        temp = Matches.objects.filter(season=season).values('team2').distinct()
        temp = [t['team2'] for t in temp]
        teams.extend(temp)
        teams  = list(set(teams))
        year_result=[]
        if kwargs.get('teamName',-1) != -1:
            teamName = kwargs.get('teamName',-1)

            years = Matches.objects.filter(Q(team1=teamName) | Q(team2=teamName)).values('season__season')
            yearsList=[]
            for year in years:
                yearsList.append(year['season__season'])
            distinctYears = sorted(list(set(yearsList)),reverse=True)
            for year in distinctYears:
                if yearsList.count(year)<=14:
                    year_result.append((year,'Leagues'))
                    continue
                lastMatch = Matches.objects.filter(season=Season.objects.get(season=year)).order_by('-match_id')[:1]
                if lastMatch[0].team1 == teamName or lastMatch[0].team2 == teamName:
                    if lastMatch[0].winner == teamName:
                        year_result.append((year, 'Winners'))
                    else:
                        year_result.append((year, 'Runners'))
                else:
                    year_result.append((year, 'Play offs'))
            if kwargs.get('matchYear', -1) == -1:
                return render(request,template_name='team_page.html',
                              context={
                                  'teams':teams,
                                  'selected_year':str(kwargs.get('season')),
                                  'seasons':self.season_list,
                                  'years':year_result,
                                  'team':kwargs.get('teamName'),
                              })
            else:
                matches = Matches.objects.filter(season=Season.objects.get(season=kwargs.get('matchYear'))).filter(Q(team1=teamName) | Q(team2=teamName)).order_by('-match_id')
                lastMatch = Matches.objects.filter(season=Season.objects.get(season=kwargs.get('matchYear'))).order_by('-match_id')[:1]
                matches_and_results = []
                for i in range(len(matches)):
                    index = len(matches)-i-1
                    if i<14:
                        matches_and_results.insert(0,(matches[index],'Leagues'))
                        continue
                    if i == len(matches)-1:
                        if lastMatch[0].team1 == teamName or lastMatch[0].team2 == teamName:
                            if lastMatch[0].winner == teamName:
                                matches_and_results.insert(0,(matches[index],'Winner'))
                            else:
                                matches_and_results.insert(0,(matches[index], 'Runners'))
                        else:
                            matches_and_results.insert(0,(matches[index], 'Play offs'))
                    else:
                        matches_and_results.insert(0,(matches[index], 'Play offs'))
                return render(request,template_name='team_page.html',context={
                    'teams':teams,
                    'seasons':self.season_list,
                    'selected_year':str(kwargs.get('season')),
                    'years':year_result,
                    'selected_season':kwargs.get('matchYear'),
                    'matches':matches_and_results,
                    'team':kwargs.get('teamName'),
                })
        return render(request,template_name='team_page.html',context={'teams':teams,'seasons':self.season_list,'selected_year':str(kwargs.get('season'))})

class HomePage(View):
    lastSeason = Season.objects.all().order_by('-season')[:1][0]
    lastMatch = Matches.objects.filter(season=lastSeason).order_by('-match_id')[:1][0]
    points = getPoints(lastSeason.season)

    def get(self,request):
        return render(request,template_name='home.html',context={'match':self.lastMatch,'points':self.points})
