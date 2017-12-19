import requests
import pandas as pd
import urllib3
from bs4 import BeautifulSoup
import csv
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 

URL1= "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period="
URL2 = "&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="

QTR_URL = [	
	"1",
	"2",
	"3",
	"4"
	]

TEAMS = [
	'ATL','BOS','BKN',
	'CHA','CHI','CLE',
	'DAL','DEN','DET',
	'GSW','HOU','IND',
	'LAC','LAL','MEM',
	'MIA','MIL','MIN',
	'NOP','NYK','OKC',
	'ORL','PHI','PHX',
	'POR','SAC','SAS',
	'TOR','UTA','WAS'
	]

colLabels = [
	'TEAM_ID',
	'TEAM_NAME',
	'GP',
	'W',
	'L',
	'W_PCT',
	'MIN',
	'OFF_RATING', # OFFENSEIVE RATING : 7
	'DEF_RATING', # DEFENSIVE RATING : 8
	'NET_RATING', # NET_RATING RATING : 9
	'AST_PCT',
	'AST_TO',
	'AST_RATIO',
	'OREB_PCT',
	'DREB_PCT',
	'REB_PCT',
	'TM_TOV_PCT',
	'EFG_PCT',
	'TS_PCT',
	'PACE',
	'PIE',
	'GP_RANK',
	'W_RANK',
	'L_RANK', 'W_PCT_RANK',
	'MIN_RANK',
	'OFF_RATING_RANK',
	'DEF_RATING_RANK',
	'NET_RATING_RANK',
	'AST_PCT_RANK',
	'AST_TO_RANK',
	'AST_RATIO_RANK',
	'OREB_PCT_RANK',
	'DREB_PCT_RANK',
	'REB_PCT_RANK',
	'TM_TOV_PCT_RANK',
	'EFG_PCT_RANK',
	'TS_PCT_RANK',
	'PACE_RANK',
	'PIE_RANK',
	'CFID',
	'CFPARAMS'
	]



#dataArray[TEAM][OFF/DEF/NET][QUARTER][q_Rtg/x_Rtg/net_Rtg]
dataArray = []
outputArray = []

for i in range(4):
	# Grab Quarterly Stats from stats.nba.com and load into list of lists
	r = requests.get(URL1 + QTR_URL[i] + URL2, headers = headers, timeout = 2)
	data = json.loads(r.text)['resultSets'][0]['rowSet']

	'''
	for d in data:
		print(str(d[1]) + " (" + colLabels[9] + ")" + ": " + str(d[9]))
	'''

	for j in range(len(TEAMS)):
		
		dataArray.append( 
		[ 
			[ 	
				#OFF 			#DEF
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ], #Q1
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ], #Q2
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ], #Q3
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]  #Q4
			], 
			[ 	
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ],
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ], 
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ], 
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
			],
			[ 	
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ],
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ], 
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ], 
				[ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
			]
		])

		# 0 : OFF_Rtg, 1: DEF_Rtg, 2:NET_Rtg
		# OFFENSEIVE RATING : 7, DEFENSIVE RATING : 8, NET_RATING RATING : 9
		dataArray[j][0][i][0] = data[j][colLabels.index('OFF_RATING')]
		dataArray[j][1][i][0] = data[j][colLabels.index('DEF_RATING')]
		dataArray[j][2][i][0] = data[j][colLabels.index('NET_RATING')]

for i in range(30):
	print(dataArray[i][2][1][0])
