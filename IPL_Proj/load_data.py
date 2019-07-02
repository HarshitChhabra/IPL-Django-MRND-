import os,django,openpyxl
os.environ.setdefault('DJANGO_SETTINGS_MODULE','IPL_Proj.settings')
django.setup()

from ipl_app.models import *

# match_data = []
# seasons = []
# wb = openpyxl.load_workbook('matches_excel.xlsx')
# ws = wb['1']
# flag=0
# for row in ws.rows:
#     if flag==0:
#         flag=1
#         continue
#     data = []
#     for cell in row:
#         data.append(cell.value)
#     data = data[:-1]
#     match_data.append(data)

#for season in list(set(seasons)):
#    seasonObj = Season(season=season)
#    seasonObj.save()

# for match in match_data:
#     season = Season.objects.get(season=match[1])
#     match[1]=season
#     match[3]=str(match[3]).split()[0]
#     if '/' in match[3]:
#         date = match[3].split('/')
#         date[2]='20'+date[2]
#         match[3]='-'.join(date[::-1])
#
#     matchObj = Matches(match_id = match[0],
#     season = match[1],
#     city = match[2],
#     date = match[3],
#     team1 = match[4],
#     team2 = match[5],
#     toss_winner = match[6],
#     toss_decision = match[7],
#     result = match[8],
#     dl_applied = match[9],
#     winner = match[10],
#     win_by_runs = match[11],
#     win_by_wickets = match[12],
#     player_of_match = match[13],
#     venue = match[14],
#     umpire1 = match[15],
#     umpire2 = match[16],
#     umpire3 = match[17])
#
#     matchObj.save()

# flag=0
# totalData = []
# inningsData = []
# oversData = []
# deliveriesData = []
# extraData = []
# deliveriesFile = openpyxl.load_workbook('deliveries_excel.xlsx')
# ws = deliveriesFile['Worksheet']
# for row in ws.rows:
#     if flag==0:
#         flag=1
#         continue
#     tempData = []
#     for cell in row:
#         tempData.append(cell.value)
#     totalData.append(tempData)
#
# for row in totalData:
#     match = Matches.objects.get(match_id=row[0])
#     inningObj = Innings(match_id=match,
#                         inning_num=row[1],
#                         batting_team=row[2],
#                         bowling_team=row[3])
#     inningObj.save()
#     #inningId = inningObj.id
#     overObj = Overs(inning = inningObj,over_num=row[4],)
#
#     inningsData.append(row[:4])
# inningsData = list(set(inningsData))
#
# for row in totalData:
#     temp = []
#     #inning = Innings.objects.get(inning_num=row[1])
#     #temp.append(inning)
#     temp.append(row[1])
#     temp.append(row[4])
#     temp.append(row[8])
#     temp.append(row[9])
#
#     oversData.append(temp)
#
#     temp = []
#     temp.append(row[4])
#     temp.extend(row[5:8])
#     temp.extend(row[10:18])
#
#
#     deliveriesData.append(temp)
#     if row[18]!='' or row[19]!='' or row[20]!='':
#         extraData.append(row[18:21])
#
# oversData = list(set(oversData))
#
# for inning in inningsData:
#     inningObj = Innings(match_id_match_id=inning[0],
#                         inning_num=inning[1],
#                         batting_team = inning[2],
#                         bowling_team = inning[3])
#     inningObj.save()
#


season = Season.objects.get(season='2019')
matches = Matches.objects.filter(season=season)
data = dict()
for match in matches:
    if data.get(match.team1,-1)==-1:
        data[match.team1]={'played':0,'won':0,'lost':0,'points':0}
    if data.get(match.team2,-1)==-1:
        data[match.team2]={'played':0,'won':0,'lost':0,'points':0}
for match in matches:
    data[match.team1]['played']+=1
    data[match.team2]['played'] += 1
    if match.winner == '':
        data[match.team1]['points']+=1
        data[match.team2]['points']+=1
    elif match.winner == match.team1:
        data[match.team1]['points']+=2
        data[match.team1]['won'] += 1
        data[match.team2]['lost']+=1
    else:
        data[match.team2]['points'] += 2
        data[match.team2]['won'] += 1
        data[match.team1]['lost'] += 1

print(data)