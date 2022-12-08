import requests
import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from nba_api.stats.static import players
from nba_api.stats.endpoints import drafthistory
from nba_api.stats.static import teams 
from nba_api.stats.endpoints import commonplayerinfo
import time

custom_headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

player_list = players.get_players()
print(player_list[24])
print(len(player_list))
player_dict = {}
num = 0
for i in range(len(player_list)):
    data_dict = {}
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = player_list[i]['id'], headers = custom_headers, timeout = 1000)
    data = player_info.common_player_info.get_json()
    player_data = json.loads(data)
    if int(player_data["data"][0][24]) >= 2000:
        data_dict["First Name"] = player_data["data"][0][1]
        data_dict["Last Name"] = player_data["data"][0][2]
        data_dict["College"] = player_data["data"][0][8]
        data_dict["Draft Year"] = player_data["data"][0][29]
        data_dict["Draft Round"] = player_data["data"][0][30]
        data_dict["Draft Pick"] = player_data["data"][0][31]
        player_dict[player_data["data"][0][0]] = data_dict
        print(data_dict)
    num += 1
    time.sleep(1)
print(player_dict)
print(len(player_dict))

# Create Relevant Draft Data List
def create_draft_data(id):
    output_list = []
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = id, headers = custom_headers, timeout = 100)
    data = player_info.common_player_info.get_json()
    player = json.loads(data)
    if int(player["data"][0][25]) > 2000:
        output_list.append(int(player["data"][0][0])) # Player ID
        output_list.append(player["data"][0][1]) # First Name
        output_list.append(player["data"][0][2]) # Last Name
        if player["data"][0][29] == "Undrafted":
            output_list.append(int(player["data"][0][25])) # Rookie Year for Undrafted Players
        else:
            output_list.append(int(player["data"][0][29])) # Draft Year
        output_list.append(player["data"][0][30]) # Draft Round
        output_list.append(player["data"][0][31]) # Draft Pick
        time.sleep(1)
    print(output_list)
    return output_list

# Create Relevant Player list (Drafted 2010-2015)
def create_yearly_player_list(year):
    output_dict = {}
    player_list = players.get_players()
    for player in player_list:
        id = player['id']
        data = create_draft_data(id)
        if data[3] == year:
            output_dict[id] = data
    return output_dict



# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# Create Player Draft Data Table
def create_draft_data_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Draft_Info (player_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, draft_year INTEGER, draft_round INTEGER, draft_pick INTEGER)") 
    conn.commit()




def main():
    #SETUP DATABASE AND TABLE
    #cur, conn = setUpDatabase('poole_party.db')
    #create_draft_data_table(cur, conn)
    a = create_yearly_player_list(2010)
    print(a)


#main()


'''id = '76006'
player_info = commonplayerinfo.CommonPlayerInfo(player_id = id, headers = custom_headers, timeout = 100)
data = player_info.common_player_info.get_json()
player = json.loads(data)
print(player)'''


#ayton = drafthistory.DraftHistory(league_id = 00, season_year_nullable = 2018, round_num_nullable = 1, round_pick_nullable = 1,
     #headers = custom_headers, timeout=3)
#print(ayton)
#team_dict = teams.get_teams()
#print(team_dict)
'''
def get_draft_pick(year, round, pick):
    base_url = f'https://stats.nba.com/stats/drafthistory?College=&LeagueID=00\
        &OverallPick=&RoundNum={round}&RoundPick={pick}&Season={year}&TeamID=&TopX='
    r = requests.get(base_url, headers = custom_headers)
    j = json.loads(r.text)
    return j'''
