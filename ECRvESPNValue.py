# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 11:49:33 2022

@author: sebas

downlaoded fantasypros adp data. csv file shows comparisons between
different adp sources within 1 table
from: https://www.fantasypros.com/nfl/adp/ppr-overall.php

goal of code is to somewhat reproduce beersheets with ranking differences
between ESPN and ECR from fantasypros, etc.

"""
import pandas as pd
import numpy as np

pd.set_option('max_rows', None)

#import csv data, sort out bye week, keep relevant to top 150 players
# rename columns to make more sense
fantasypros = pd.read_csv( 'E:\Fantasy\ADPs\FantasyPros2022.csv').rename(
    columns = {'Rank' : 'FPros', 'Player' : 'Player Name'}).iloc[0:150, : ]
fantasypros = fantasypros[['Player Name', 'FPros', 'RTSports', 'Fantrax',
       'FFC', 'Sleeper', 'AVG']]

fantasypros.FPros = fantasypros.FPros.astype(float)

#importing ESPN ADP from API, see "getting ESPNadp.py"

ESPN = pd.read_csv('E:\Fantasy\ADPs\ESPNADP.csv', index_col = 0)

##merge ffpros data with espn file from API
##renaming avgADP from ESPN file to ESPN
test = fantasypros.merge(ESPN, on = 'Player Name')
test = test[['Player Name', 'Position', 'AvgADP', 'FPros',  'RTSports', 'Fantrax',
       'FFC', 'Sleeper', 'AVG']].rename(columns = {'AvgADP' : 'ESPN'})


## recalculate avg adp/ECR ADP by excluding already included ESPN data
test['ECR'] = test[['FPros',  'RTSports', 'Fantrax',
       'FFC', 'Sleeper']].mean(axis=1)

## defining new column to get value from new avg/ECR v espn data
##i.e consensus ADP versus ESPN
test['Value'] = test['ECR'] - test['ESPN']

#keep relevant columns
test = test[['Player Name', 'Position','FPros', 'ESPN', 'RTSports', 'Fantrax', 'FFC', 'Sleeper',
        'ECR', 'Value']]

# for visibility small df with name, pos, espn rankings, ECR and value in comparison to espn
# sort by ECR

value = test[['Player Name', 'Position', 'ESPN', 'ECR', 'Value']].sort_values(by = ['ECR'])

#bit messy but create a list for a separate index to use for "ranking" of
# draft adivce for when to draft players according to ECR
# same thing as ECR just, but is visually quicker to pick up on


value['index'] = list(range( 0, 129))
rank = ((value['index'] + 12) / 12)
value['round'] = rank.apply(np.floor).astype(int)
value['pick'] = ((rank - value['round'] + 0.084) * 12 ).apply(np.floor).astype(int)

#combine round and pick
cols = ['round', 'pick']
value['Round|Pick'] = value[cols].apply(lambda row: '|'.join(row.values.astype(str)), axis = 1)


## dump index, round and pick, should give us final table to use for draft
value = value[['Player Name', 'Position', 'ESPN', 'ECR', 'Value', 'Round|Pick']]

positions = np.unique(value['Position'])

qb_only = value.loc[value['Position'] == 'QB'] # 14
rb_only = value.loc[value['Position'] == 'RB'] # 41
wr_only = value.loc[value['Position'] == 'WR'] # 57
te_only = value.loc[value['Position'] == 'TE'] # 16

value.reset_index(drop = True)
value.to_csv('ECRvESPNValue.csv', index= False)


