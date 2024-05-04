import pandas as pd
from typing import Literal

def read_data(team, type):
    if type=='shots':
        team_directory = team.replace(' ', '_')
        df = pd.read_csv(f'data/understat/{team_directory}/2023/shots/all_shots_data.csv')
    elif type=='match':
        team_directory = team.replace(' ', '_')
        df = pd.read_csv(f'data/understat/{team_directory}/2023/matches/PL_matches.csv')

    return df

def get_match_details(home_team, away_team):
    home_matches = read_data(home_team, 'match')
    match_info = home_matches[
        (home_matches['h.title']==home_team) & (home_matches['a.title']==away_team)
        ]
    date = match_info['datetime'].values[0].split(' ')[0]
    home_goals = match_info['goals.h'].values[0].astype('int')
    away_goals = match_info['goals.a'].values[0].astype('int')
    home_xg = match_info['xG.h'].values[0]
    away_xg = match_info['xG.a'].values[0]

    return date, home_goals, away_goals, home_xg, away_xg

def get_xg_plot_data(df, home_team, away_team):
    shots_data = df[(df['h_team']==home_team) & (df['a_team']==away_team)]
    shots_data['X'] = shots_data['X'].astype(float)*100
    shots_data['Y'] = shots_data['Y'].astype(float)*100
    shots_data['xG_scaled'] = shots_data['xG'].astype(float) * 1500

    return shots_data

def get_team_data(df, home_or_away: Literal['h','a']):
    goals = df[(df['result']=='Goal') & (df['h_a']==home_or_away)]
    non_goals = df[(df['result']!='Goal') & (df['h_a']==home_or_away)]
    total_shots = len(goals.index) + len(non_goals.index)

    return goals, non_goals, total_shots

