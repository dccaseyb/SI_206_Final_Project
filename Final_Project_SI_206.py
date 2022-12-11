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
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = player_list[i]['id'], headers = custom_headers, timeout = 100)
    data = player_info.common_player_info.get_json()
    player_data = json.loads(data)
    if player_data["data"][0][-4] == "Undrafted" or player_data["data"][0][24] == None: # or player_data["data"][0][24] == None, check if this works then remove from line 49
        pass
        '''if player_data["data"][0][24] == None:
            pass
        elif int(player_data["data"][0][24]) >= 2000:
            data_dict["First Name"] = player_data["data"][0][1]
            data_dict["Last Name"] = player_data["data"][0][2]
            data_dict["College"] = player_data["data"][0][8]
            data_dict["Draft Year"] = player_data["data"][0][24]
            data_dict["Draft Round"] = player_data["data"][0][-3]
            data_dict["Draft Pick (Overall)"] = player_data["data"][0][-2]
            player_dict[player_data["data"][0][0]] = data_dict
            print(data_dict)'''
    #elif player_data["data"][0][24] == None:
        #pass
    elif int(player_data["data"][0][-4]) >= 2010 and int(player_data["data"][0][-4]) <= 2015:
        data_dict["First Name"] = player_data["data"][0][1]
        data_dict["Last Name"] = player_data["data"][0][2]
        data_dict["College"] = player_data["data"][0][8]
        data_dict["Draft Year"] = player_data["data"][0][-4]
        data_dict["Draft Round"] = player_data["data"][0][-3]
        data_dict["Draft Pick (Overall)"] = player_data["data"][0][-2]
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
def create_player_list():
    output_dict = {}
    player_list = players.get_players()
    for player in range(len(player_list)):
        id = player[i]['id']
        data = create_draft_data(id)
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

# Insert Players into Table

# MUST FIND AWAY TO  LIMIT IT TO 25 PLAYERS EACH TIME
def add_drafted_players(cur, conn):
    drafted_player_list = create_player_list()
    for player in drafted_player_list:
        id = player.index() #find how to get the index for the id
        f_name = player["First Name"]
        l_name = player["Last Name"]
        year = player["Draft Year"]
        round = player["Draft Pick"]
        if round == 2:
            pick = player["Draft Pick (Overall)"] - 30
        else:
            pick = player["Draft Pick (Overall)"]
        cur.execute("INSERT OR IGNORE INTO Draft_Info (player_id, first_name, last_name, draft_year, draft round, draft pick) VALUES (?,?,?,?,?,?)",
            (id, f_name, l_name, year, round, pick))
    conn.commit()





def main():
    #SETUP DATABASE AND TABLE
    #cur, conn = setUpDatabase('poole_party.db')
    #create_draft_data_table(cur, conn)
    a = create_yearly_player_list(2010)
    print(a)


#main()


'''id = '1629071'
player_info = commonplayerinfo.CommonPlayerInfo(player_id = id, headers = custom_headers, timeout = 100)
data = player_info.common_player_info.get_json()
player = json.loads(data)
print(player)
print((player["data"][0][24]))'''


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

'''player_list = players.get_players()
print(player_list[24])
print(len(player_list))
player_dict = {}
num = 0
for i in range(len(player_list)):
    data_dict = {}
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = player_list[i]['id'], headers = custom_headers, timeout = 100)
    data = player_info.common_player_info.get_json()
    player_data = json.loads(data)
    print(player_data)
    player_dict[player_list[i]['id']] = player_data
    #time.sleep(1)'''

'''player_list = players.get_players()
print(player_list[24])
print(len(player_list))
player_dict = {}
num = 0
for i in range(len(player_list)):
    data_dict = {}
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = player_list[i]['id'], headers = custom_headers, timeout = 100)
    data = player_info.common_player_info.get_json()
    player_data = json.loads(data)
    print(player_data)
    time.sleep(1)'''

'''player_list = players.get_players()
#print(player_list)
player_info = commonplayerinfo.CommonPlayerInfo(player_id = player_list[24]['id'], headers = custom_headers, timeout = 100)
data = player_info.common_player_info.get_json()
player_data = json.loads(data)
print(player_data)
'''
