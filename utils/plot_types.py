import matplotlib.pyplot as plt

from utils.plot_utils import Plotter
from utils.data_utils import read_data, get_match_details, get_xg_plot_data, get_team_data
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
    'Liverpool': ['red','white'],
    'Luton Town': ['darkorange','white'],
    'Manchester United': ['red','black'],
    'Manchester City': ['deepskyblue','white'],
    'Newcastle United': ['black','white'],
    'Nottingham Forest': ['red','white'],
    'Sheffield United': ['red','white'],
    'Tottenham': ['white','navy'],
    'West Ham': ['purple','lightblue'],
    'Wolverhampton Wanderers': ['gold','black']
}

class HalfPitchHomeAwayShots:
    def __init__(self, home_team, away_team, scrape: bool=True):
        self.home_team = home_team
        self.away_team = away_team
        self.scrape = scrape

        self.date, self.total_home_goals, self.total_away_goals, self.total_home_xg, self.total_away_xg = get_match_details(
            self.home_team, self.away_team)

        if self.scrape:
            self.data = get_shot_data(self.home_team, self.away_team)
        else:
            self.data = read_data(home_team, 'shots')
        # MAKE THE FOLLOWING THREE STEPS MORE EFFICIENT
        self.match_shots_data = get_xg_plot_data(self.data, self.home_team, self.away_team)
        self.home_goals, self.home_non_goals, self.total_home_shots = get_team_data(
            self.match_shots_data, 'h')
        self.away_goals, self.away_non_goals, self.total_away_shots = get_team_data(
            self.match_shots_data, 'a')

        self.plot = Plotter(plt)
        self.pitch = self.plot.pitch_type('half_pitch')
        self.fig, self.axs = self.plot.make_plot_grid(self.pitch)

        self.home_goal_sc, self.home_non_goal_sc = self.plot.plot_scatter(
            self.pitch, self.home_goals, self.home_non_goals, team_colours[home_team][0], team_colours[home_team][1], 
            self.axs['pitch'][0])
        self.away_goal_sc, self.away_non_goal_sc = self.plot.plot_scatter(
            self.pitch, self.away_goals,self. away_non_goals, team_colours[away_team][0], team_colours[away_team][1], 
            self.axs['pitch'][1])

        self.plot.plot_multi_main_text(
            self.axs, title=f'{self.home_team} v {self.away_team} | {self.total_home_goals}-{self.total_away_goals} | Premier League | {self.date}')
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

        self.date, self.total_home_goals, self.total_away_goals, self.total_home_xg, self.total_away_xg = get_match_details(
            self.home_team, self.away_team)

        if self.scrape:
            self.data = get_shot_data(self.home_team, self.away_team).reset_index(drop=True)
        else:
            self.data = read_data(home_team, 'shots').reset_index(drop=True)

        #TODO: make data_utils methods for the below
        #now that we have our dataframe set up, we are going to create some lists to plot the different xG values
        #4 lists - home and away xg and minutes
        #We start these with zero so our charts will start at 0
        a_xG = [0]
        h_xG= [0]
        a_min = [0]
        h_min = [0]

        #this finds our team names from the dataframe. This will only work as long as both teams took a shot
        hteam = self.data['h_team'].iloc[0]
        ateam = self.data['a_team'].iloc[0]

        for x in range(len(self.data['xG'])):
            if self.data['h_a'][x]=='h':
                h_xG.append(float(self.data['xG'][x]))
                h_min.append(int(self.data['minute'][x]))
            if self.data['h_a'][x]=='a':
                a_xG.append(float(self.data['xG'][x]))
                a_min.append(int(self.data['minute'][x]))

        #this is the function we use to make our xG values be cumulative rather than single shot values
        #it goes through the list and adds the numbers together
        def nums_cumulative_sum(nums_list):
            return [sum(nums_list[:i+1]) for i in range(len(nums_list))]

        h_cumulative = nums_cumulative_sum(h_xG)
        a_cumulative = nums_cumulative_sum(a_xG)

        # make a common final value for both sets of mins
        if h_min[-1]<=90 and a_min[-1]<=90:
            h_min.append(90)
            h_xG.append(h_xG[-1])
            a_min.append(90)
            a_xG.append(a_xG[-1])
        if h_min[-1]==90 and a_min[-1]<90:
            a_min.append(90)
            a_xG.append(a_xG[-1])
        if h_min[-1]<90 and a_min[-1]==90:
            h_min.append(90)
            h_xG.append(h_xG[-1])
        if h_min[-1]>90 and a_min[-1]>90:
            if h_min[-1]>a_min[-1]:
                a_min.append(h_min[-1])
            a_xG.append(a_xG[-1])
            if h_min[-1]<a_min[-1]:
                h_min.append(a_min[-1])
                h_xG.append(h_xG[-1])

        #this is used to find the total xG. It just creates a new variable from the last item in the cumulative list
        hlast = round(h_cumulative[-1],2)
        alast = round(a_cumulative[-1],2)

        self.plot = Plotter(plt)
        self.fig, self.axs = self.plot.make_normal_plot()

        self.axs.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
        spines = ['top','bottom','left','right']
        for x in spines:
            if x in spines:
                self.axs.spines[x].set_visible(False)
                
        self.axs.set_xticks([0,15,30,45,60,75,90])
        self.axs.set_xlabel('Minute', color='black', fontsize=14)
        self.axs.set_ylabel('xG', color='black', fontsize=14)

        #plot the step graphs
        self.axs.step(x=h_min,y=h_cumulative,color='black',label=ateam,linewidth=5,where='post')
        self.axs.step(x=a_min,y=a_cumulative,color='purple',label=ateam,linewidth=5,where='post')

        self.plot.save_figure(self.fig, self.home_team, self.away_team, self.date, 'xg_flow')
