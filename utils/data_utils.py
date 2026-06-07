import pandas as pd
import numpy as np
from typing import Literal

def read_data(team, type):
    if type=='shots':
        team_directory = team.replace(' ', '_')
        df = pd.read_csv(f'data/understat/{team_directory}/2024/shots/all_shots_data.csv')
    elif type=='match':
        team_directory = team.replace(' ', '_')
        df = pd.read_csv(f'data/understat/{team_directory}/2024/matches/PL_matches.csv')

    return df

def get_match_details(home_team, away_team):
    home_matches = read_data(home_team, 'match')
    match_info = home_matches[
        (home_matches['h.title']==home_team) & (home_matches['a.title']==away_team)
        ]
    date = match_info['datetime'].values[0].split(' ')[0]
    # date = (lambda x: x[2]+'-'+x[1]+'-'+x[0])(match_info['datetime'].values[0].split(' ')[0])
    home_goals = match_info['goals.h'].values[0].astype('int')
    away_goals = match_info['goals.a'].values[0].astype('int')
    home_xg = match_info['xG.h'].values[0]
    away_xg = match_info['xG.a'].values[0]

    return date, home_goals, away_goals, home_xg, away_xg

def get_xg_plot_data(df, home_team, away_team, half_pitch):
    shots_data = df[(df['h_team']==home_team) & (df['a_team']==away_team)]
    shots_data.to_csv('shots_data.csv')
    if half_pitch==True:
        shots_data['X'] = shots_data['X'].astype(float)*100
        shots_data['Y'] = shots_data['Y'].astype(float)*100
    else:
        shots_data['X'].loc[shots_data['h_a']=='h'] = (1 - shots_data['X'].astype(float))*100
        shots_data['Y'].loc[shots_data['h_a']=='h'] = (1 - shots_data['Y'].astype(float))*100
        shots_data['X'].loc[shots_data['h_a']=='a'] = shots_data['X'].astype(float)*100
        shots_data['Y'].loc[shots_data['h_a']=='a'] = shots_data['Y'].astype(float)*100
    shots_data['xG_scaled'] = shots_data['xG'].astype(float) * 1500

    return shots_data

def get_team_data(df, home_or_away: Literal['h','a']):
    goals = df[(df['result']=='Goal') & (df['h_a']==home_or_away)]
    non_goals = df[(df['result']!='Goal') & (df['h_a']==home_or_away)]
    total_shots = len(goals.index) + len(non_goals.index)

    return goals, non_goals, total_shots

def get_xg_flow_data(df):
    a_xG = [0]
    h_xG= [0]
    a_min = [0]
    h_min = [0]
    df.reset_index(inplace=True)

    for x in range(len(df['xG'])):
        if df['h_a'][x]=='h':
            h_xG.append(float(df['xG'][x]))
            h_min.append(int(df['minute'][x]))
        if df['h_a'][x]=='a':
            a_xG.append(float(df['xG'][x]))
            a_min.append(int(df['minute'][x]))

    if h_min[-1]<=90 and a_min[-1]<=90:
        h_min.append(90)
        h_xG.append(0)
        a_min.append(90)
        a_xG.append(0)
    if h_min[-1]>=90 and a_min[-1]<90:
        a_min.append(h_min[-1])
        a_xG.append(0)
    if h_min[-1]<90 and a_min[-1]>=90:
        h_min.append(a_min[-1])
        h_xG.append(0)
    if h_min[-1]>=90 and a_min[-1]>=90:
        if h_min[-1] > a_min[-1]:
            a_min.append(h_min[-1])
            a_xG.append(0)
        elif h_min[-1] < a_min[-1]:
            h_min.append(a_min[-1])
            h_xG.append(0)
        else:
            pass

    h_cumulative = [sum(h_xG[:i+1]) for i in range(len(h_xG))]
    a_cumulative = [sum(a_xG[:i+1]) for i in range(len(a_xG))]

    return h_cumulative, h_min, a_cumulative, a_min