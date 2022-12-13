# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import array
import numpy as np
import time
import sqlite3
import json
import os
import re
import sys

plt.style.use('seaborn')
years = [2017, 2018, 2019, 2020, 2021]
player_draft_pick = []
player_win_shares = []
player_draft_year = []

#year = 2019


def scrape_data():
    for year in years:
        k=0
        url = f"https://www.basketball-reference.com/draft/NBA_{year}.html"
        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        headers = [th.getText() for th in soup.findAll("tr", limit=2)[1].findAll("th")]
        headers = headers[1:]
        rows = soup.findAll("tr")[1:]
        draft_player_stats = {}
        draft_player_stats[year] = {}
        for i in range(len(rows)):
            tds = rows[i].findAll("td")
            if len(tds) > 0:
                h = 0
                name = tds[2].getText()
                draft_player_stats[year][name] = {}
                for td in tds:
                    draft_player_stats[year][name][headers[h]] = td.getText()
                    h += 1
            #print(draft_player_stats[year][name])
                draft_pick = draft_player_stats[year][name][headers[0]]
                win_shares = draft_player_stats[year][name][headers[17]]
                player_draft_pick.insert(k, draft_pick)
                player_win_shares.insert(k, win_shares)
                player_draft_year.insert(k, year)
            #print(year, draft_pick, win_shares)
        k+=1
    

def removeNull(row):
    return ['0' if i== '' else i for i in row]

player_win_shares = removeNull(player_win_shares)
player_win_shares = [float(i) for i in player_win_shares]
player_draft_pick = [int(i) for i in player_draft_pick]
#print(player_draft_pick)


#print(player_draft_pick)   
#print(player_win_shares)     
#print(player_draft_year)



def final_data():
    draft_data = tuple(zip(player_draft_year, player_draft_pick, player_win_shares))
    print(str(draft_data))


def draw_graph():
    plt.scatter(player_draft_pick, player_win_shares, s = 8, c = player_draft_year,
          cmap = plt.cm.get_cmap("cool", 5), edgecolors= "k")
    cbar = plt.colorbar(ticks=[2017, 2018, 2019, 2020, 2021])
    #cbar.set_label(label = "Year Drafted", size = 10)
    plt.xlabel("Draft Pick")
    plt.ylabel("Win Share Value")
    plt.title("Draft Picks vs Win-Shares for Players Drafted from 2017-2021")
    plt.yticks(fontsize=5)
    plt.xticks(fontsize = 5)
    plt.show()






















#draft_table = soup.find("table", {"id":"stats"})[0]
#rows = draft_table.findAll("tr")
#print(draft_table)


#def scrape_NBA_draft_data(years):
    #final_df = pd.DataFrame(columns = ["Pk", "Player", "Yrs", "G",
                                       #"MP", "PTS", "WS", "BPM",
                                       #"VORP"])

#years = list(range(2016, 2022))
#years
#headers = {'User-Agent': 'Mozilla/5.0'}
    #for y in years:
        #year = y
#url = r"https://www.basketball-reference.com/draft/NBA_2021.html"
#source  = requests.get(url, headers=headers)
#soup = BeautifulSoup(source.content, features="lxml")
#soup.findAll('tr', limit =2 )
#header = [th.getText() for th in soup.findAll('tr', limit = 2)[0].findAll('th')]

 

    
