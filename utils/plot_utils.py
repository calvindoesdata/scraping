import os
from matplotlib.patches import Ellipse
from mplsoccer import Pitch, VerticalPitch
from typing import Tuple

class Plotter:
    def __init__(self, plt):
        self.plt=plt

        # Define plot parameters
        plt.rcParams['axes.facecolor'] = '#E5E0E0'
        plt.rcParams['figure.facecolor'] = '#E5E0E0'
        plt.rcParams['text.color'] = 'black'

    def pitch_type(self, half_pitch: bool):
        if half_pitch:
            pitch = VerticalPitch(
                pitch_type='opta', pad_bottom=0.5, half=half_pitch, goal_type='box', goal_alpha=0.8)
        else:
            pitch = Pitch(
                pitch_type='opta', goal_type='box', goal_alpha=0.8)
        
        return pitch

    def make_plot_grid(self, pitch):
        if pitch.half==True:
            fig, axs = pitch.grid(
                figheight=9, ncols=2, endnote_height=0.00, endnote_space=0,
                axis=False, title_height=0.08, grid_height=0.84)
        else:
            fig, axs = pitch.grid(
                figheight=9, ncols=1, endnote_height=0.03, endnote_space=0,
                axis=False, title_height=0.00, grid_height=0.84)
        
        return fig, axs
    
    def make_normal_plot(self):
        fig, ax = self.plt.subplots(figsize = (9,5))

        return fig, ax
    
    def plot_scatter(self, pitch, goals_df, non_goals_df, primary_colour, secondary_colour, ax):
        sc_non_goals = pitch.scatter(
            non_goals_df.X, non_goals_df.Y, s=non_goals_df.xG_scaled,
            edgecolors='#606060', c=primary_colour, marker='o', ax=ax)
        sc_goals = pitch.scatter(
            goals_df.X, goals_df.Y, s=goals_df.xG_scaled,
            edgecolors='#606060', c=secondary_colour, marker='o', ax=ax, zorder=1)
        
        return sc_goals, sc_non_goals
        
    def plot_multi_main_text(self, axs, title, main_x, main_y, main_fontsize, secondary_x, secondary_y, secondary_fontsize):
        axs.text(x=main_x, y=main_y, s=title, ha="center", va="center", fontsize=main_fontsize, fontweight='bold', color='black')

        self.plt.text(x=secondary_x, y=secondary_y,
                 s='Data from Understat.\nChart by @gavdoesdata.',
                 fontsize=secondary_fontsize, color='black')

    def plot_multi_axes_text(self, ax, title, title_elements, colours, half_pitch, home=False):
        if half_pitch:
            ax_title = ax.text(100, 101, title, ha='left', va='center', fontsize=14, fontweight='bold')
            for element, colour in zip(title_elements, colours):
                ax_title = ax.annotate(element + ' ', xycoords=ax_title, xy=(1, 0), verticalalignment="bottom",
                                       fontsize=15, color=colour, weight="bold")
        else:
            if home:
                coords, h_justification = (0,102), 'left'
            else:
                coords, h_justification = (100,102), 'left'
            ax_title = ax.text(coords[0], coords[1], title, ha=h_justification, va='center', fontsize=14, fontweight='bold')
            for element, colour in zip(title_elements, colours):
                ax_title = ax.annotate(element + ' ', xycoords=ax_title, xy=(1, 0), verticalalignment="bottom",
                                       fontsize=15, color=colour, weight="bold")
            
    def plot_multi_axes_shots_text(self, ax, elements, half_pitch=False, home=False):
        if half_pitch:
            ax.text(x=1.5, y=51, s=f'Total shots: {elements[0]}\nTotal xG: {elements[1]:.1f}', 
                    fontsize=15, fontweight='bold', horizontalalignment='right')
        else:
            if home:
                ax.text(x=49, y=1.5, s=f'Total shots: {elements[0]}\nTotal xG: {elements[1]:.1f}', 
                        fontsize=14, fontweight='bold', horizontalalignment='right')
            else:
                ax.text(x=51, y=1.5, s=f'Total shots: {elements[0]}\nTotal xG: {elements[1]:.1f}', 
                        fontsize=14, fontweight='bold', horizontalalignment='left')

    def plot_single_axis_header(self, ax, home_team, away_team, home_goals, away_goals, match_date):
        # ax.text(x=50, y=98.5, s=f'{home_team} v {away_team}\n{str(home_goals)} - {str(away_goals)}', 
        #         fontsize=22, fontweight='bold', horizontalalignment='center', verticalalignment='top')
        teams_len_diff = len(home_team) - len(away_team)
        # if teams_len_diff > 0:
        #     home_team = abs(teams_len_diff)*' ' + home_team
        # elif teams_len_diff < 0:
        #     away_team = away_team + abs(teams_len_diff)*' '
        ax.text(x=50, y=98.5, s=f'{home_team} | {str(home_goals)} - {str(away_goals)} | {away_team}', 
                fontsize=22, fontweight='bold', horizontalalignment='center', verticalalignment='top')
        ax.text(x=50, y=93, s=f'Premier League | {match_date}', 
                fontsize=16, fontweight='bold', horizontalalignment='center', verticalalignment='top')

    def plot_single_axis_shots_text(self, ax, home_elements, away_elements):
        ax.text(x=50, y=1.5, s=f'{home_elements[0]} <- Shots -> {away_elements[0]}\n{home_elements[1]:.1f} <- xG -> {away_elements[1]:.1f}', 
                fontsize=14, fontweight='bold', horizontalalignment='center')

    def plot_legend(self, plt_or_ax, chart_objects_list, labels):
        leg = plt_or_ax.legend(chart_objects_list, labels, ncol=1, frameon=True, fontsize=12,
            handlelength=2, bbox_to_anchor=(0.945,0.025), borderpad=1.1,
            handletextpad=1, scatterpoints = 1)
    
    def plot_marker_scale_legend(self, plt, fig):
        def _circle(center, height, width):
            center = center
            height = height
            width = width
            ellipse = Ellipse(center, width, height, facecolor='white', edgecolor='black', linewidth=1.5)
            fig.add_artist(ellipse)

        circle_1 = _circle((0.9225,0.92), 0.05, 0.020)
        circle_2 = _circle((0.8775,0.92), 0.025, 0.010)

        plt.annotate("xG", xy=(0.1, 0.2), xycoords=fig.transFigure, xytext=(0.89225, 0.885), fontsize=12, fontweight='bold', zorder=3)
        plt.annotate("", xy=(0.91, 0.919), xycoords=fig.transFigure, xytext=(0.888, 0.919), arrowprops=dict(arrowstyle="->", lw=2, color='black'), zorder=4)
        #plt.annotate("", xy=(0.95, 2), xytext=(0.90, 29), arrowprops=dict(arrowstyle="->", lw=2, color='black'), zorder=2)

    def save_figure(self, fig, home_team, away_team, date, plot_type, year):
        if not os.path.exists(os.path.join('output')):
            os.mkdir(os.path.join('output'))
        home_team = home_team.replace(' ','_')
        away_team = away_team.replace(' ','_')
        fig.savefig(f'output/{year}/{plot_type}_{home_team}_{away_team}_{date}.png', 
                    dpi=500, bbox_inches='tight')