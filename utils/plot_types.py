import matplotlib.pyplot as plt

from utils.plot_utils import Plotter
from utils.data_utils import read_data, get_match_details, get_xg_plot_data, get_team_data, get_xg_flow_data
from utils.scraping_utils import get_shot_data

#TODO: add variable initialisation (e.g. title coords) for different plot types in the plot_type classes, carry over to plot_utils methods

# CHANGE TO PRIMARY COLOUR FOR SHOTS AND GIVE EVERYONE THE SAME GOAL COLOUR, LESS CONFUSING IN PLOTS
team_colours = {
    'Arsenal': ['red','white'],
    'Aston Villa': ['darkmagenta','lightblue'],
    'Bournemouth': ['red','black'],
    'Brentford': ['red','white'],
    'Brighton': ['dodgerblue','white'],
    'Burnley': ['purple','lightblue'],
    'Chelsea': ['blue','white'],
    'Crystal Palace': ['royalblue','red'],
    'Everton': ['mediumblue','white'],
    'Fulham': ['white','black'],
    'Leicester': ['blue','white'],
    'Liverpool': ['red','white'],
    'Luton Town': ['darkorange','white'],
    'Manchester United': ['red','black'],
    'Manchester City': ['deepskyblue','white'],
    'Newcastle United': ['black','white'],
    'Nottingham Forest': ['red','white'],
    'Sheffield United': ['red','white'],
    'Southampton': ['red','white'],
    'Tottenham': ['white','navy'],
    'West Ham': ['purple','lightblue'],
    'Wolverhampton Wanderers': ['gold','black'],

    'England': ['white','red'],
    'Slovakia': ['lightblue','white']
}

class HalfPitchHomeAwayShots:
    def __init__(self, home_team, away_team, scrape: bool=True):
        self.home_team = home_team
        self.away_team = away_team
        self.scrape = scrape

        if self.scrape:
            self.date, self.total_home_goals, self.total_away_goals, self.total_home_xg, self.total_away_xg, self.data = \
                get_shot_data(self.home_team, self.away_team)
        else:
            self.date, self.total_home_goals, self.total_away_goals, self.total_home_xg, self.total_away_xg = get_match_details(
                self.home_team, self.away_team)
            self.data = read_data(home_team, 'shots')
        # MAKE THE FOLLOWING THREE STEPS MORE EFFICIENT
        self.match_shots_data = get_xg_plot_data(self.data, self.home_team, self.away_team)
        self.home_goals, self.home_non_goals, self.total_home_shots = get_team_data(
            self.match_shots_data, 'h')
        self.away_goals, self.away_non_goals, self.total_away_shots = get_team_data(
            self.match_shots_data, 'a')

        self.plot = Plotter(plt)
        self.pitch = self.plot.pitch_type(half_pitch=True)
        self.fig, self.axs = self.plot.make_plot_grid(self.pitch)

        self.home_goal_sc, self.home_non_goal_sc = self.plot.plot_scatter(
            self.pitch, self.home_goals, self.home_non_goals, team_colours[home_team][0], team_colours[home_team][1], 
            self.axs['pitch'][0])
        self.away_goal_sc, self.away_non_goal_sc = self.plot.plot_scatter(
            self.pitch, self.away_goals,self. away_non_goals, team_colours[away_team][0], team_colours[away_team][1], 
            self.axs['pitch'][1])

        self.plot.plot_multi_main_text(
            self.axs['title'], title=f'{self.home_team} v {self.away_team} | {self.total_home_goals}-{self.total_away_goals} | Premier League | {self.date}', 
            main_x=+0.5, main_y=+0.4, main_fontsize=26, secondary_x=0, secondary_y=0, secondary_fontsize=9)
        self.plot.plot_multi_axes_text(self.axs['pitch'][0], title=f'{self.home_team} | ', title_elements=['Shots', 'and', 'Goals'], 
                          colours=[team_colours[home_team][0], 'black', team_colours[home_team][1]])
        self.plot.plot_multi_axes_text(self.axs['pitch'][1], title=f'{self.away_team} | ', title_elements=['Shots', 'and', 'Goals'], 
                          colours=[team_colours[away_team][0], 'black', team_colours[away_team][1]])
        self.plot.plot_multi_axes_shots_text(self.axs['pitch'][0], [self.total_home_shots, self.total_home_xg])
        self.plot.plot_multi_axes_shots_text(self.axs['pitch'][1], [self.total_away_shots, self.total_away_xg])

        self.plot.save_figure(self.fig, self.home_team, self.away_team, self.date, 'shot_map')

class XGFlow:
    def __init__(self, home_team, away_team, scrape: bool=True):
        self.home_team = home_team
        self.away_team = away_team
        self.scrape = scrape

        if self.scrape:
            self.date, self.total_home_goals, self.total_away_goals, self.total_home_xg, self.total_away_xg, self.data = \
                get_shot_data(self.home_team, self.away_team)
        else:
            self.date, self.total_home_goals, self.total_away_goals, self.total_home_xg, self.total_away_xg = get_match_details(
                self.home_team, self.away_team)
            self.data = read_data(home_team, 'shots')

        h_cumulative, h_min, a_cumulative, a_min = get_xg_flow_data(self.data)

        self.plot = Plotter(plt)
        self.fig, self.axs = self.plot.make_normal_plot()

        self.axs.grid(ls='dotted',lw=.5,color='grey',axis='y',zorder=1)
        spines = ['top','bottom','left','right']
        for x in spines:
            if x in spines:
                self.axs.spines[x].set_visible(False)

        self.axs.set_xticks([0,15,30,45,60,75,90])
        self.axs.set_xlabel('Minute', color='black', fontsize=11)
        self.axs.set_ylabel('xG', color='black', fontsize=11)

        title_height = max(h_cumulative[-1], a_cumulative[-1]) + 0.25

        self.plot.plot_multi_main_text(
            self.axs, f'{self.home_team} v {self.away_team} | {self.total_home_goals}-{self.total_away_goals} | Premier League | {self.date}', 
            main_x=+45, main_y=+title_height, main_fontsize=14, secondary_x=+90, secondary_y=-0.5, secondary_fontsize=6)

        self.axs.step(x=h_min,y=h_cumulative,color=team_colours[self.home_team][0],
                      label=self.home_team,linewidth=3,where='post')
        self.axs.step(x=a_min,y=a_cumulative,color=team_colours[self.away_team][0],
                      label=self.away_team,linewidth=3,where='post')

        self.plot.save_figure(self.fig, self.home_team, self.away_team, self.date, 'xg_flow')

class SofaScoreHomeAwayShots():
    def __init__(self, home_team, away_team, home_goals, home_non_goals, away_goals, away_non_goals, 
                 total_home_shots, total_away_shots, total_home_goals, total_away_goals, total_home_xg, total_away_xg, 
                 date):
        self.home_team = home_team
        self.away_team = away_team
        self.home_goals = home_goals
        self.home_non_goals = home_non_goals
        self.away_goals = away_goals
        self.away_non_goals = away_non_goals
        self.total_home_shots = total_home_shots
        self.total_away_shots = total_away_shots
        self.total_home_goals = total_home_goals
        self.total_away_goals = total_away_goals
        self.total_home_xg = total_home_xg
        self.total_away_xg = total_away_xg
        self.date = date

        self.plot = Plotter(plt)
        self.pitch = self.plot.pitch_type(half_pitch=True)
        self.fig, self.axs = self.plot.make_plot_grid(self.pitch)

        self.home_goal_sc, self.home_non_goal_sc = self.plot.plot_scatter(
            self.pitch, self.home_goals, self.home_non_goals, team_colours[home_team][0], team_colours[home_team][1], 
            self.axs['pitch'][0])
        self.away_goal_sc, self.away_non_goal_sc = self.plot.plot_scatter(
            self.pitch, self.away_goals,self. away_non_goals, team_colours[away_team][0], team_colours[away_team][1], 
            self.axs['pitch'][1])

        self.plot.plot_multi_main_text(
            self.axs['title'], title=f'{self.home_team} v {self.away_team} | {self.total_home_goals}-{self.total_away_goals} | Euros Championship | {self.date}', 
            main_x=+0.5, main_y=+0.4, main_fontsize=26, secondary_x=0, secondary_y=0, secondary_fontsize=9)
        self.plot.plot_multi_axes_text(self.axs['pitch'][0], title=f'{self.home_team} | ', title_elements=['Shots', 'and', 'Goals'], 
                          colours=[team_colours[home_team][0], 'black', team_colours[home_team][1]])
        self.plot.plot_multi_axes_text(self.axs['pitch'][1], title=f'{self.away_team} | ', title_elements=['Shots', 'and', 'Goals'], 
                          colours=[team_colours[away_team][0], 'black', team_colours[away_team][1]])
        self.plot.plot_multi_axes_shots_text(self.axs['pitch'][0], [self.total_home_shots, self.total_home_xg])
        self.plot.plot_multi_axes_shots_text(self.axs['pitch'][1], [self.total_away_shots, self.total_away_xg])

        self.plot.save_figure(self.fig, self.home_team, self.away_team, self.date, 'shot_map')