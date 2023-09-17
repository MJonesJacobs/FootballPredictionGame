import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import datetime
from db_link import DB_CURSOR, DB_CONNECTION, all_teams
from TeamLogos import LOGOS
from pathlib import Path
import pandas as pd
from tkinter import *
from dataclasses import dataclass
from PIL import Image, ImageTk

PLOT_HEIGHT = 20

# Data Imports
@dataclass
class PlayerBarGraphInfo():
    player : str
    categories : list
    values : list
    
    def __post_init__(self):
        assert len(self.categories)==len(self.values), "Number of values not equal to number of categories"

def image_matrix(team:str,height:float):
    image = Image.open(Path(LOGOS[team]))
    a = np.asarray(image)
    return a
    
def scale_image(image:OffsetImage)->None:
    image.set_height(PLOT_HEIGHT)

def team_points(player:str,season:str)->PlayerBarGraphInfo:
    teams = all_teams(season=season)
    data = pd.DataFrame(columns=["Team","Total Score"])
    data["Team"] = teams.copy()
    player_scores = list()
    total_scores = list()
    for team in teams:
        player_scores.append(DB_CURSOR.execute(f"""SELECT SUM(Points) FROM '{season}' WHERE (HomeTeam = ? OR AwayTeam = ?) AND Player = ? AND ResultAdded = 1""",(team,team,player)).fetchone()[0])
        total_scores.append(DB_CURSOR.execute(f"""SELECT SUM(Points) FROM '{season}' WHERE (HomeTeam = ? OR AwayTeam = ?) AND ResultAdded = 1""",(team,team)).fetchone()[0])
        
    data["Player Score"]=player_scores
    data["Total Score"] = total_scores
    data = data.sort_values(by="Total Score",ascending=FALSE)
    
    return PlayerBarGraphInfo(player,data["Team"].to_list(),data["Player Score"].to_list())

def bar_plot(plot_info:list[PlayerBarGraphInfo]):
    assert all(plot_data.categories == plot_info[0].categories for plot_data in plot_info), "The categories are not the same"
    
    fig, ax = plt.subplots(figsize=(10,5))

    x = plot_info[0].categories
    X_axis = np.arange(len(x))
    bar_width = 0.1
    centre = (len(plot_info)*-(bar_width/2)) + (bar_width/2)
    for plot in plot_info:
        y = plot.values
        ax.bar(X_axis + centre, y, bar_width, label = plot.player)
        centre += bar_width
    
    ax.set_xticks(X_axis)
    # ax.set_xticklabels(x,rotation=90)
    ax.set_xlabel("Team")
    ax.set_ylabel("Points")
    ax.set_title("Total Points per Team")
    ax.legend()
    
    
    img = [image_matrix(ii,PLOT_HEIGHT) for ii in x]

    tick_labels = ax.xaxis.get_ticklabels()

    for i,im in enumerate(img):
        ib = OffsetImage(im, zoom=0.5)
        scale_image(ib)
        ib.image.axes = ax
        ab = AnnotationBbox(ib, (X_axis[i],0),frameon=False, xycoords='data',  boxcoords="offset points", pad=0, box_alignment=(0.5,0.5))
        ax.add_artist(ab)
    
        
        pass
    plt.show()

player_info = list()
for player in ["Matt","Simon"]:
    player_info.append(team_points(player=player,season="2023_24"))

bar_plot(plot_info=player_info)