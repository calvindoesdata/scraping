import re
import os
import json
import requests

import pandas as pd

from bs4 import BeautifulSoup

def get_matches(home_team, away_team):
    team = home_team.replace(' ','_')
    response = requests.get(f'https://understat.com/team/{team}/2024')

    soup = BeautifulSoup(response.text, 'html.parser')
    ugly_soup = str(soup)

    match_id_data = re.search("var datesData .*= JSON.parse\('(.*)'\)", ugly_soup).group(1)
    data = json.loads(match_id_data.encode('utf8').decode('unicode_escape'))

    match_id_df = pd.json_normalize(data)

    match = match_id_df[
        (match_id_df['h.title']==home_team) & (match_id_df['a.title']==away_team)]
    
    date = match['datetime'].values[0].split(' ')[0]
    home_goals = int(match['goals.h'].values[0])
    away_goals = int(match['goals.a'].values[0])
    home_xg = float(match['xG.h'].values[0])
    away_xg = float(match['xG.a'].values[0])
    match_id = match['id'].values[0]

    return date, home_goals, away_goals, home_xg, away_xg, match_id

def get_shot_data(home_team, away_team):
    date, home_goals, away_goals, home_xg, away_xg, match_id = get_matches(home_team, away_team)
    response = requests.get(f'https://understat.com/match/{match_id}')
    soup = BeautifulSoup(response.text, 'html.parser')
    ugly_soup = str(soup)

    shots_data = re.search("var shotsData .*= JSON.parse\('(.*)'\)", ugly_soup).group(1)

    data = json.loads(shots_data.encode('utf8').decode('unicode_escape'))

    home_shots = pd.DataFrame(data['h'])
    away_shots = pd.DataFrame(data['a'])

    match_shots_df = pd.concat([home_shots,away_shots]).reset_index(drop=True)

    return date, home_goals, away_goals, home_xg, away_xg, match_shots_df
