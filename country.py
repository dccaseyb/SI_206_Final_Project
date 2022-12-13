import requests
import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt


def getResponse(cur, conn):

    url = "https://api-nba-v1.p.rapidapi.com/players"


    headers = {
        "X-RapidAPI-Key": "c504582aaamsh7b209b153427ebap16dc45jsna7b47cb2d1ca",
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    for i in range(1,32):
        querystring = {"team": i,"season":"2021"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        response_info = json.loads(response.text)

        if(response_info.get('response') == None):
            continue

        for r in response_info['response']:
            start_year = r['nba']['start']
            if(start_year >= 2017):
                first_name = r['firstname']
                last_name = r['lastname']
                country = r['birth']['country']
                id = r['id']
                addToTable(cur, conn, id, start_year, first_name, last_name, country)


def addToTable(cur, conn, id, s, f, l, c):

    # cur.execute("SELECT count(country) FROM Country_info")
    # if(( cur.fetchall()[0][0] - count[0] ) >= 25):
    #     print("EXITS")
    #     exit(0)
    # else:
    cur.execute("INSERT OR IGNORE INTO Country_Info (id, start, first_name, last_name, country) VALUES (?,?,?,?,?)", (id, s, f, l, c))
    conn.commit()

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def calculate(cur, conn):
    f = open("countries.txt", "w")
    cur.execute("SELECT count(country) FROM Country_info")
    f.write("Total NBA Players examined: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'USA'")
    f.write("Players from USA: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country != 'USA'")
    f.write("Players from outside USA: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Serbia'")
    f.write("Players from Serbia: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Germany'")
    f.write("Players from Germany: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Finland'")
    f.write("Players from Finland: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'France'")
    f.write("Players from France: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Turkey'")
    f.write("Players from Turkey: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Slovenia'")
    f.write("Players from Slovenia: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'South Sudan'")
    f.write("Players from South Sudan: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Sudan'")
    f.write("Players from Sudan: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Lithuania'")
    f.write("Players from Lithuania: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Angola'")
    f.write("Players from Angola: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'United Kingdom'")
    f.write("Players from United Kingdom: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Gabon'")
    f.write("Players from Gabon: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Argentina'")
    f.write("Players from Argentina: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Australia'")
    f.write("Players from Australia: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Jamaica'")
    f.write("Players from Jamaica: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Montenegro'")
    f.write("Players from Montenegro: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Bahamas'")
    f.write("Players from Bahamas: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Nigeria'")
    f.write("Players from Nigeria: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Japan'")
    f.write("Players from Japan: " + str(cur.fetchall()[0][0]) +'\n')
    cur.execute("SELECT count(country) FROM Country_info WHERE country = 'Canada'")
    f.write("Players from Canada: " + str(cur.fetchall()[0][0]) +'\n')
    f.close()


def draw_graph():
    labels = 'USA', 'FRA', 'GER', 'LTU', 'All Others'
    sizes = [127, 3, 2, 2, 17]
    explode = (0, 0.3, 0.2, 0.1, 0.05)
    fig1, (ax1,ax2) = plt.subplots(1,2)
    patches, texts, autotexts = ax1.pie(sizes, explode = explode, labels = labels, autopct = '%1.2f%%', shadow = False, radius = 1, startangle= 180)
    ax1.axis('equal')
    ax1.set_title("All incoming NBA talent by country (2017-2021)", verticalalignment = 'bottom')

    labels = 'SRB', 'GER', 'FIN', 'FRA', 'TUR','SVN', 'SSD','SDN', 'LTU','ANG', 'UK', 'GAB', 'ARG', 'AUS', 'JAM', 'MNE', 'BHS', 'NGA', 'JPN', 'CAN'
    sizes = [1, 2, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    explode = (0, 0.1, 0, 0.1, 0, 0, 0, 0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    patches, texts, autotexts = ax2.pie(sizes, explode = explode, labels = labels, autopct = '%1.2f%%', shadow = False, radius = 1)
    ax2.axis('equal')
    ax2.set_title("All incoming foreign NBA talent (2017-2021)", verticalalignment = 'top')

    plt.setp(autotexts, size='x-small')
    plt.show()

def main():
    #SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('poole_party.db')
    cur.execute("DROP TABLE IF EXISTS Country_Info") 
    cur.execute("CREATE TABLE IF NOT EXISTS Country_Info (id INTEGER PRIMARY KEY, start INTEGER, first_name TEXT, last_name TEXT, country TEXT)") 
    conn.commit()

    getResponse(cur, conn)
    calculate(cur, conn)
    draw_graph()

if __name__ == "__main__":
    main()