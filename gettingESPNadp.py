# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 10:02:48 2022

@author: sebas

first 40 lines mostly taken from github (https://gist.github.com/dtcarls/c6158cd8ad41e0941571807052098a0f) to access ESPN API to get ESPN ADP for 2022
certain values changed, year in url, filename, most importantly:
changed from auctionvalue date to get averagedraftposition as well as
position id for the players, see pos_change
second half of the code used to change position ID from int to str position
issue: uncertain about what scoring format these values are for
matches ESPN ADP website, does not match ESPN MOCK draft lobbies!

^fantasypros has a version of ESPN ADP, slightly mismatches my dataset
fp also says ESPN ADP can be found under PPR scoring, so likely default for their rankings

default was player limit 150, see line 29 "req.add_header", 
can change value of "limit" to pull more data
"""

import urllib.request 
import json 
import csv
import pandas as pd
import numpy as np

year = 2022
req = urllib.request.Request(f'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leaguedefaults/3?view=kona_player_info')
req.add_header('x-fantasy-filter','{"players":{"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"limit":200,"offset":0,"sortAverageAuction":{"sortAsc":false,"sortPriority":1},"sortDraftRanks":{"sortPriority":100,"sortAsc":true,"value":"STANDARD"},"filterRanksForScoringPeriodIds":{"value":[1]},"filterRanksForRankTypes":{"value":["PPR"]},"filterRanksForSlotIds":{"value":[0,2,4,6,17,16]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002021","102021","002020","022021"]}}}')
with urllib.request.urlopen(req) as url:
    data = json.loads(url.read().decode())
    print(data)

with open('adp.txt','w') as outfile:
    json.dump(data,outfile)

with open('adp.txt') as json_file:
    with open('snakeADP.csv', mode='w') as auction_file:
        auction_file.write("Name, Position, Value")
        auction_file.write('\n')
        data = json.load(json_file)
        for person in data['players']:
            if person['player']['ownership']['averageDraftPosition'] > 1:
                auction_file.write(person['player']['fullName']+","+str(person[
                    'player']['defaultPositionId']) + "," + str(person['player'][
                        'ownership']['averageDraftPosition']))
                auction_file.write('\n')
        
#-----change position values from int to str via dict.
snakeADP = pd.read_csv('snakeADP.csv')

snakeADP.dtypes

pos_change = { 1 : "QB", 2: "RB", 3: "WR", 4: "TE", 5: "K", 16: "DST"}


snakeADP[" Position"].replace(pos_change, inplace = True)

# round down numbers for value column
decimals = 2
snakeADP[" Value"] = snakeADP[" Value"].apply(lambda x: round(x, decimals))
snakeADP = snakeADP.rename(columns = {'Name' : 'Player Name', ' Position' : 'Position', ' Value' : 'AvgADP'})

snakeADP.to_csv('ESPNADP1.csv')

