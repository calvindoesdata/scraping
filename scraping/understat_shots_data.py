import re
import os
import json
import requests

import pandas as pd

from bs4 import BeautifulSoup

for subdir, dirs, files in os.walk('/Users/calvinwraith/Projects/scraping/data/understat/'):
    if '2024' in dirs:
        match_ids = pd.read_csv(os.path.join(subdir, '2024', 'matches', 'PL_matches.csv'))

        played_match_ids = match_ids[match_ids['isResult']==True]['id'].tolist()

        team = subdir.split('/')[-1]

        all_match_shots_dfs = []

        for match in played_match_ids:
            response = requests.get(f'https://understat.com/match/{match}')
            soup = BeautifulSoup(response.text, 'html.parser')
            ugly_soup = str(soup)

            shots_data = re.search("var shotsData .*= JSON.parse\('(.*)'\)", ugly_soup).group(1)

            data = json.loads(shots_data.encode('utf8').decode('unicode_escape'))

            home_shots = pd.DataFrame(data['h'])
            away_shots = pd.DataFrame(data['a'])

            match_shots_df = pd.concat([home_shots,away_shots])
            all_match_shots_dfs.append(match_shots_df)

        if not os.path.exists(os.path.join(subdir,'2024','shots')):
            os.mkdir(os.path.join(subdir,'2024','shots'))
        all_match_shots_df = pd.concat(all_match_shots_dfs)
        all_match_shots_df.to_csv(os.path.join(subdir,'2024','shots',f'all_shots_data.csv'), index=False)
