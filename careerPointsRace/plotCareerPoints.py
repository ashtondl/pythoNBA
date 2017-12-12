import matplotlib.pyplot as plt, mpld3
#import seaborn as sns
import numpy as np
import pandas as pd
import math

RECORD = 38387

players = [
	'Kareen_Abdul-Jabbar',
	'LeBron_James',
	'Kevin_Durant',
	'Stephen_Curry',
	'Russell_Westbrook',
	'James_Harden',
	'Kyrie_Irving',
]

projection = [
	'LeBron_James'
]

folder = 'Player_Data\\'
plt.style.use('fivethirtyeight')

plt.figure(figsize=(14,12))
for i, file_name in enumerate(players):
    player_name = file_name.split("_")[0] + " " + file_name.split("_")[1]
    current_df = pd.read_csv(folder + file_name + ".csv")
    plt.plot(current_df.GAME_CAREER, current_df.TOTAL_3MADE, label=player_name, lw=4.0)

for i, file_name in enumerate(projection):
	proj_name = file_name.split("_")[0] + " " + file_name.split("_")[1] + " (Projected Points)"
	df = pd.read_csv(folder + file_name + ".csv")
	games_played = df.tail(1).values[0,2]
	total_points = df.tail(1).values[0,3]
	cPPG = round(df.tail(1).values[0,3] / df.tail(1).values[0,2], 2)
	print( proj_name + ": " + str( cPPG ))

	games_needed = math.ceil((RECORD - total_points) / cPPG)
	projected_x = [ games_played ]
	projected_y = [ total_points ]
	for j in range (1, games_needed + 1):
		projected_x.append( projected_x[j-1] + 1 )
		projected_y.append( math.trunc(total_points + (cPPG * j) ) )

	plt.plot(projected_x, projected_y, label=proj_name, lw=4.0, linestyle=':')
	
	bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="cyan", ec="b", lw=2)
	#plt.annotate('Current Games: %s' % projected_x[0], xy=(projected_x[0], projected_y[0]), size=20, bbox=bbox_props )
	#plt.annotate('Record: %s' % projected_x[-1], xy=(projected_x[-1], projected_y[-1]), size=20 )

plt.legend(loc = 0)

plt.title("Career Points vs. Games Played", fontsize=24)

plt.ylim([0, 40000])
plt.xlim([0, 1600])

plt.xlabel("Games Played", fontsize=20)
plt.ylabel("Career Points", fontsize=20)

plt.savefig('career_points_race.png', bbox_inches='tight')

mpld3.show()