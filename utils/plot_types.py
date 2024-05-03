import matplotlib.pyplot as plt

from utils.plot_utils_dev import Plotter
from utils.data_utils import read_data, get_match_details, get_xg_plot_data, get_team_data

# CHANGE TO PRIMARY COLOUR FOR SHOTS AND GIVE EVERYONE THE SAME GOAL COLOUR, LESS CONFUSING IN PLOTS
team_colours = {
    'Arsenal': ['red','white'],
    'Burnley': ['purple','lightblue'],
    'Crystal Palace': ['royalblue','red'],
    'Newcastle United': ['black','white'],
    'Sheffield United': ['red','white'],
    'Tottenham': ['white','navy']
}

class HalfPitchHomeAwayShots:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

        self.date, self.total_home_goals, self.total_away_goals, self.total_home_xg, self.total_away_xg = get_match_details(
            self.home_team, self.away_team)

        self.data = read_data(home_team, 'shots')
        self.match_shots_data = get_xg_plot_data(self.data, self.home_team, self.away_team)
        self.home_goals, self.home_non_goals, self.total_home_shots = get_team_data(
            self.match_shots_data, 'h')
        self.away_goals, self.away_non_goals, self.total_away_shots = get_team_data(
            self.match_shots_data, 'a')

        self.plot = Plotter(plt)
        self.fig, self.axs = self.plot.make_plot_grid()

        self.home_goal_sc, self.home_non_goal_sc = self.plot.plot_scatter(
            self.home_goals, self.home_non_goals, team_colours[home_team][0], team_colours[home_team][1], 
            self.axs['pitch'][0])
        self.away_goal_sc, self.away_non_goal_sc = self.plot.plot_scatter(
            self.away_goals,self. away_non_goals, team_colours[away_team][0], team_colours[away_team][1], 
            self.axs['pitch'][1])
        
        self.plot.plot_multi_main_text(
            self.axs, title=f'{self.home_team} v {self.away_team} | {self.total_home_goals}-{self.total_away_goals} | Premier League | {self.date}')
        self.plot.plot_multi_axes_text(self.axs['pitch'][0], title=f'{self.home_team} | ', title_elements=['Shots', 'and', 'Goals'], 
                          colours=[team_colours[home_team][0], 'black', team_colours[home_team][1]])
        self.plot.plot_multi_axes_text(self.axs['pitch'][1], title=f'{self.away_team} | ', title_elements=['Shots', 'and', 'Goals'], 
                          colours=[team_colours[away_team][0], 'black', team_colours[away_team][1]])
        self.plot.plot_multi_axes_shots_text(self.axs['pitch'][0], [self.total_home_shots, self.total_home_xg])
        self.plot.plot_multi_axes_shots_text(self.axs['pitch'][1], [self.total_away_shots, self.total_away_xg])

        self.plot.save_figure(self.fig, self.home_team, self.away_team, self.date)