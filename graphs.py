import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import datetime
from db_link import DB_CURSOR, DB_CONNECTION, all_teams
from TeamLogos import LOGOS
from pathlib import Path
import pandas as pd
from tkinter import *
from tkinter import ttk
from dataclasses import dataclass
from PIL import Image, ImageTk
import datetime
from abc import ABC, abstractmethod

PLOT_HEIGHT = 20
DATE_STRING =  "%d/%m/%Y"



def cumulative_sum(list1):
    sum_list = []
    sum = 0
    for i in range(len(list1)):
        sum += list1[i]
        sum_list.append(sum)
    return sum_list

def date_plot(player:str,season:int)->list[list,list]:
    plot_info = DB_CURSOR.execute(f"""SELECT Date, SUM(Points) FROM '{season}' WHERE Player = ? AND ResultAdded = 1 GROUP BY Date""",(player,)).fetchall()
    plot_list = list()
    for date,score in plot_info:
        plot_list.append([datetime.datetime.strptime(date, DATE_STRING),score])
        
    plot_info = sorted(plot_list, key=lambda x: x[0])
    cum_sum = 0 
    dates = list()
    scores = list()
    for date,score in plot_info:
        cum_sum += score
        dates.append(date)
        scores.append(cum_sum)
                
    return [dates,scores]
    

# # Data Imports
# @dataclass
# class PlayerBarGraphInfo():
#     player : str
#     categories : list
#     values : list
    
#     def __post_init__(self):
#         assert len(self.categories)==len(self.values), "Number of values not equal to number of categories"

# def image_matrix(team:str,height:float):
#     image = Image.open(Path(LOGOS[team]))
#     a = np.asarray(image)
#     return a
    
# def scale_image(image:OffsetImage)->None:
#     image.set_height(PLOT_HEIGHT)

# def team_points(player:str,season:str)->PlayerBarGraphInfo:
#     teams = all_teams(season=season)
#     data = pd.DataFrame(columns=["Team","Total Score"])
#     data["Team"] = teams.copy()
#     player_scores = list()
#     total_scores = list()
#     for team in teams:
#         player_scores.append(DB_CURSOR.execute(f"""SELECT SUM(Points) FROM '{season}' WHERE (HomeTeam = ? OR AwayTeam = ?) AND Player = ? AND ResultAdded = 1""",(team,team,player)).fetchone()[0])
#         total_scores.append(DB_CURSOR.execute(f"""SELECT SUM(Points) FROM '{season}' WHERE (HomeTeam = ? OR AwayTeam = ?) AND ResultAdded = 1""",(team,team)).fetchone()[0])
        
#     data["Player Score"]=player_scores
#     data["Total Score"] = total_scores
#     data = data.sort_values(by="Total Score",ascending=FALSE)
    
#     return PlayerBarGraphInfo(player,data["Team"].to_list(),data["Player Score"].to_list())

# def bar_plot(plot_info:list[PlayerBarGraphInfo]):
#     assert all(plot_data.categories == plot_info[0].categories for plot_data in plot_info), "The categories are not the same"
    
#     fig, ax = plt.subplots(figsize=(10,5))

#     x = plot_info[0].categories
#     X_axis = np.arange(len(x))
#     bar_width = 0.1
#     centre = (len(plot_info)*-(bar_width/2)) + (bar_width/2)
#     for plot in plot_info:
#         y = plot.values
#         ax.bar(X_axis + centre, y, bar_width, label = plot.player)
#         centre += bar_width
    
#     ax.set_xticks(X_axis)
#     # ax.set_xticklabels(x,rotation=90)
#     ax.set_xlabel("Team")
#     ax.set_ylabel("Points")
#     ax.set_title("Total Points per Team")
#     ax.legend()
    
    
#     img = [image_matrix(ii,PLOT_HEIGHT) for ii in x]

#     tick_labels = ax.xaxis.get_ticklabels()

#     for i,im in enumerate(img):
#         ib = OffsetImage(im, zoom=0.5)
#         scale_image(ib)
#         ib.image.axes = ax
#         ab = AnnotationBbox(ib, (X_axis[i],0),frameon=False, xycoords='data',  boxcoords="offset points", pad=0, box_alignment=(0.5,0.5))
#         ax.add_artist(ab)
    
        
#         pass
#     plt.show()

# player_info = list()
# for player in ["Matt","Simon"]:
#     player_info.append(team_points(player=player,season="2023_24"))

# bar_plot(plot_info=player_info)

# x = list(range(100))
# y = list(range(100))
# plt.plot(x,y)
# plt.show()
# for player in ["Matt","Simon"]:
#     dates, scores = date_plot(player,"2023_24")
#     plt.plot(dates,scores)
# plt.show()

@dataclass
class PlotInfo():
    name: str
    x :list
    y :list
    color : str
    marker : str = "o"
    linestyle : str = "solid"
    
    def __post_init__(self):
        assert len(self.x) == len(self.y), "Lengths of x and y must be equal!"

@dataclass
class PlotFormatting():
    title: str
    x_title: str
    y_title: str      


    
class DisplayGraph():
    fig_width = 15
    fig_height = 10
    
    def __init__(self,master_frame:Frame,plots:list[PlotInfo],formatting:PlotFormatting=None):
        
        self.figure = Figure(figsize=(self.fig_width,self.fig_height),dpi=100)
        self.master_frame = master_frame
        
        self.plot = self.figure.add_subplot(111)
        for plot in plots:
            self.plot.plot(plot.x,plot.y,color = plot.color, marker = plot.marker, linestyle = plot.linestyle)
        
        if formatting != None:
            self.figure.suptitle(formatting.title)
            self.figure.set_
                        
        canvas = FigureCanvasTkAgg(self.figure, master = master_frame)
        
        canvas.draw() 
        # creating the Matplotlib toolbar 
        toolbar = NavigationToolbar2Tk(canvas,master_frame) 
        toolbar.update() 
    
        # placing the toolbar on the Tkinter window 
        canvas.get_tk_widget().pack()
    
        
class GraphFrame():
    graph_options = ["Select Graph Type","Cumulative Score"]
    def __init__(self,master_frame:Frame) -> None:
        
        self.master_frame = master_frame
        self.master_frame.rowconfigure(0,weight=0)
        self.master_frame.rowconfigure(1,weight=1)
        
        # Control Frame
        self.control_frame = Frame(self.master_frame)
        self.control_frame.grid(column=0,row=0,columnspan=2,sticky="nsew")
        
        self.plot_type = StringVar()
        plot_label = Label(self.control_frame,text="Plot Type:")
        plot_label.grid(row=0,column=0,sticky="e")
        self.plot_type_menu = ttk.OptionMenu(self.control_frame,self.plot_type,*self.graph_options)
        self.plot_type_menu.grid(row=0,column=1,sticky="w")
        self.plot_type.trace("w",self.trace_plot)
        
    def generate_graph(self,plots:list[PlotInfo],formatting:PlotFormatting = None):
        if hasattr(self,"graph_frame"):
            self.graph_frame.destroy()
        self.graph_frame = LabelFrame(self.master_frame,text="Graph Test Frame")
        self.graph_frame.grid(column=0,row=1,columnspan=2,sticky="nsew")
        
        DisplayGraph(self.graph_frame,plots=plots)
    
    def trace_plot(self,*args):
        if self.plot_type.get() == "Cumulative Score":
            plots = list()
            for player,color in [["Matt","r"],["Simon","b"]]:
                plot_x,plot_y = date_plot(player=player,season="2023_24")
                plots.append(PlotInfo(
                    name=player,
                    x = plot_x,
                    y = plot_y,
                    color= color,
                    
                ))
            self.generate_graph(plots)
        
        
if True:
    pass