import re
import os
import json
import requests

import pandas as pd

from bs4 import BeautifulSoup

response = requests.get('https://understat.com/league/EPL')

soup = BeautifulSoup(response.text, 'html.parser')
ugly_soup = str(soup)

team_id_data = re.search("var teamsData .*= JSON.parse\('(.*)'\)", ugly_soup).group(1)
data = json.loads(team_id_data.encode('utf8').decode('unicode_escape'))

for k,v in data.items():
    team = v['title'].replace(' ','_')
    response = requests.get(f'https://understat.com/team/{team}/2023')

    soup = BeautifulSoup(response.text, 'html.parser')
    ugly_soup = str(soup)

    match_id_data = re.search("var datesData .*= JSON.parse\('(.*)'\)", ugly_soup).group(1)
    data = json.loads(match_id_data.encode('utf8').decode('unicode_escape'))

    match_id = pd.json_normalize(data)
    if not os.path.exists(os.path.join('data','understat',team,'2023')):
        os.mkdir(os.path.join('data','understat',team,'2023'))
        if not os.path.exists(os.path.join('data','understat',team,'2023','matches')):
            os.mkdir(os.path.join('data','understat',team,'2023','matches'))
    match_id.to_csv(f'data/understat/{team}/2023/matches/PL_matches.csv', index=False)

# response = requests.get('https://understat.com/team/Newcastle_United/2023')

# soup = BeautifulSoup(response.text, 'html.parser')
# ugly_soup = str(soup)

# match_id_data = re.search("var datesData .*= JSON.parse\('(.*)'\)", ugly_soup).group(1)
# data = json.loads(match_id_data.encode('utf8').decode('unicode_escape'))

# match_id = pd.json_normalize(data)
# match_id.to_csv('data/understat/nufc_matches.csv', index=False)

