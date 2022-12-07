import requests
import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from nba_api.stats.static import players

player_dict = players.get_json()


