# File for generating a dashboard of all teams so that team specific info can be added

from pathlib import Path
from tkinter import Frame, LabelFrame, CENTER, END, LEFT, PhotoImage
from tkinter.ttk import Treeview, Style
from db_link import season_teams
from App_Formatting.formatting_conventions import frame_padx,frame_pady
from TeamLogos import TeamImage, LOGOS
from time import sleep

class TeamDashboard():
    def __init__(self,master_frame:Frame,season:str) -> None:
        
        teams = season_teams(season)
        # Frames
        master_frame.rowconfigure(0,weight=1)
        master_frame.columnconfigure(0,weight=0)
        master_frame.columnconfigure(1,weight=1)

        # Team Selection Frame
        self.all_team_frame = LabelFrame(master=master_frame,text="All Teams")
        self.all_team_frame.grid(row=0,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.all_team_frame.rowconfigure(0,weight=1)
        
        # Dashboard Frame
        self.team_dashboard_frame = LabelFrame(master=master_frame,text="Team Info")
        self.team_dashboard_frame.grid(row=0,column=1,sticky="nsew",padx=frame_padx,pady=frame_pady)

        # Populate Frames

        # Table Frame

        columns = ["Team"]
        global images
        images = dict()
        for x in teams:
            img = TeamImage(x)
            img.resize_img(0.8)
            images.update({x:img})

        s = Style()
        s.configure('Treeview', rowheight=50)
        self.tree = Treeview(self.all_team_frame, columns=columns, show="tree")
        for i,col in enumerate(columns):
            self.tree.heading(i,text=col)
        self.tree.column("#0",minwidth=0,width=50)
        self.tree.column(0,width=100,anchor=CENTER)
        # Iterate over the rows in the Pandas DataFrame and add each row to the Treeview widget
        for i, team in enumerate(teams):
            if i % 2 == 0:
                self.tree.insert("", END, image=images[team].photoimage, values=(team,), tags=('evenrow',))
            else:
                self.tree.insert("", END, image=images[team].photoimage, values=(team,), tags=('oddrow',))
        self.tree.tag_configure('oddrow', background='white smoke')
        self.tree.tag_configure('evenrow', background='snow')
        self.tree.grid(row=0,column=0,sticky="nsew")
        self.tree.bind('<ButtonRelease-1>',self.selectedItem)

    
    def selectedItem(self, *args):
        self.selectedsec = self.tree.focus()
        self.secitem = self.tree.set(self.selectedsec)
        print(f"Selected Item is {self.secitem}")
