import requests
import pandas as pd
import urllib3
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.basketball-reference.com/"
GAME_LOG_DIR = '/gamelog/'
PLAYER_PROFILE_PAGE = ".html"

players_dict = {
	'Kareen Abdul-Jabbar' : 'players/a/abdulka01',
	'LeBron James' : 'players/j/jamesle01',
	'Kevin Durant' : 'players/d/duranke01',
	'Carmelo Anthony' : 'players/a/anthoca01',
	'Stephen Curry' : 'players/c/curryst01',
	'Russell Westbrook' : 'players/w/westbru01',
	'Damian Lillard' : 'players/l/lillada01',
	'James Harden' : 'players/h/hardeja01',
	'Kyrie Irving' : 'players/i/irvinky01',
	'Blake Griffin' : 'players/g/griffbl01',
	'Vince Carter' : 'players/c/cartevi01',
	'Pau Gasol' : 'players/g/gasolpa01',
	'Joe Johnson' : 'players/j/johnsjo02',
	'Jason Terry' : 'players/t/terryja01',
	'Tony Parker' : 'players/p/parketo01'
}

players_list = [
	'Kareen Abdul-Jabbar',
	'LeBron James',
	'Kevin Durant',
	'Carmelo Anthony',
	'Stephen Curry',
	'Russell Westbrook',
	'Damian Lillard',
	'James Harden',
	'Kyrie Irving',
	'Blake Griffin',
	'Vince Carter',
	'Pau Gasol',
	'Joe Johnson',
	'Jason Terry',
	'Tony Parker'
]

csv_list = [
	'Kareen_Abdul-Jabbar',
	'LeBron_James',
	'Kevin_Durant',
	'Carmelo_Anthony',
	'Stephen_Curry',
	'Russell_Westbrook',
	'Damian_Lillard',
	'James_Harden',
	'Kyrie_Irving',
	'Blake_Griffin',
	'Vince_Carter',
	'Pau_Gasol',
	'Joe_Johnson',
	'Jason_Terry',
	'Tony_Parker'
]

def getSoupFromURL(url):
	try:
		r = requests.get(url)
	except:
		return None

	return BeautifulSoup(r.text, "html5lib")


def get_data_for_game_log(player, season):
    string_season = str(int(season.split("-")[0]) + 1)
    return BASE_URL + players_dict[player] + GAME_LOG_DIR + string_season

def get_data_for_player(player):
    return BASE_URL + players_dict[player] + PLAYER_PROFILE_PAGE

seasons_for_players = []

for player in players_list:
    soup = getSoupFromURL(get_data_for_player(player))
    table = soup.find('table', attrs={"class" : "row_summable"})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    seasons = []
    for row in rows:
        season_column = row.find('th', attrs={"data-stat" : "season"})
        season_text = season_column.text
        if season_text not in seasons:
            seasons.append(season_text)
    seasons_for_players.append(seasons)

for player, seasons, file_name in zip(players_list, seasons_for_players, csv_list):
    game_count = 0
    points_sum = 0
    list_rows = []
    for season in seasons:
        soup = getSoupFromURL(get_data_for_game_log(player, season))
        table = soup.find('table', attrs={"class" : "row_summable"})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            point = row.find('td', attrs={"data-stat" : "pts"})
            if point is None:
                continue
            game_count += 1
            points_sum += int(point.text)
            list_rows.append([player, game_count, points_sum])
    data_frame = pd.DataFrame(data=list_rows, columns=['PLAYER_NAME', 'GAME_CAREER', 'TOTAL_3MADE'])
    path = ''
    data_frame.to_csv(file_name + ".csv", header=True)