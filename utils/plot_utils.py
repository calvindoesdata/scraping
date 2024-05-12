import os
from matplotlib.patches import Ellipse
from mplsoccer import VerticalPitch

class Plotter:
    def __init__(self, plt):
        self.plt=plt

        # Define plot parameters
        plt.rcParams['axes.facecolor'] = '#E5E0E0'
        plt.rcParams['figure.facecolor'] = '#E5E0E0'
        plt.rcParams['text.color'] = 'black'

    def pitch_type(self, half_pitch: bool):
        vertical_pitch = VerticalPitch(
            pitch_type='opta', pad_bottom=0.5, half=half_pitch, goal_type='box', goal_alpha=0.8)
        
        return vertical_pitch

    def make_plot_grid(self, pitch):
        fig, axs = pitch.grid(
            figheight=9, ncols=2, endnote_height=0.03, endnote_space=0,
            axis=False, title_height=0.08, grid_height=0.84)
        
        return fig, axs
    
    def make_normal_plot(self):
        fig, ax = self.plt.subplots(figsize = (10,5))

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

    def plot_multi_axes_text(self, ax, title, title_elements, colours):
        ax_title = ax.text(100, 101, title, ha='left', va='center', fontsize=14, fontweight='bold')
        for element, colour in zip(title_elements, colours):
            ax_title = ax.annotate(element + ' ', xycoords=ax_title, xy=(1, 0), verticalalignment="bottom", 
                                   fontsize=15, color=colour, weight="bold")
            
    def plot_multi_axes_shots_text(self, ax, elements):
        ax.text(x=1.5, y=51, s=f'Total shots: {elements[0]}\nTotal xG: {elements[1]:.1f}', 
                fontsize=15, fontweight='bold', horizontalalignment='right')

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

    def save_figure(self, fig, home_team, away_team, date, plot_type):
        if not os.path.exists(os.path.join('output')):
            os.mkdir(os.path.join('output'))
        home_team = home_team.replace(' ','_')
        away_team = away_team.replace(' ','_')
        fig.savefig(f'output/{plot_type}_{home_team}_{away_team}_{date}.png', 
                    dpi=500, bbox_inches='tight')