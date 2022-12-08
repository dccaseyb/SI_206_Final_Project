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

player_list = players.get_active_players()
print(player_list[24])
for i in range(10):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = player_list[i]['id'], headers = custom_headers, timeout = 100)
    data = player_info.common_player_info.get_json()
    player_data = json.loads(data)
    print("ID: " + str(player_data["data"][0][0]))
    print("First Name: " + player_data["data"][0][1])
    print("Last Name: " + player_data["data"][0][2])
    print("College: " + player_data["data"][0][8])
    print("Draft Year: " + str(player_data["data"][0][29]))
    print("Draft Round: " + str(player_data["data"][0][30]))
    print("Draft Pick: " + str(player_data["data"][0][31]))

# Create Relevant Draft Data List
def create_draft_data(id):
    output_list = []
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = id, headers = custom_headers, timeout = 100)
    data = player_info.common_player_info.get_json()
    player = json.loads(data)
    output_list.append(int(player["data"][0][0])) # Player ID
    output_list.append(player["data"][0][1]) # First Name
    output_list.append(player["data"][0][2]) # Last Name
    if player["data"][0][29] == "Undrafted":
        output_list.append(int(player["data"][0][24])) # Rookie Year for Undrafted Players
    else:
        output_list.append(int(player["data"][0][29])) # Draft Year
    output_list.append(player["data"][0][30]) # Draft Round
    output_list.append(player["data"][0][31]) # Draft Pick
    return output_list

# Create Relevant Player list (Drafted 2010-2015)
def create_yearly_player_list(year):
    output_list = []
    player_list = players.get_players()
    for player in player_list:
        id = player['id']
        data = create_draft_data(id)
        if data[3] == year:
            output_list.append(data)
    return output_list



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
