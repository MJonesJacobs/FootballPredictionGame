from tkinter import *
from tkinter import ttk
from typing import Any
from db_link import player_list, DB_CURSOR, DB_CONNECTION
from tkinter_functions import clear_subframes
from App_Formatting.formatting_conventions import frame_padx,frame_pady
from web_scrape import get_gw_info, FixtureData
from tkinter import messagebox


class PredictionRow():
    def __init__(self, player:str,gameweek:int, scape_data:FixtureData) -> None:
        self.gameweek = gameweek
        self.player = player
        self.hometeam = scape_data.home_team
        self.awayteam = scape_data.away_team
        self.home_prediction = IntVar()
        self.home_prediction.trace("w",self.trace_home_prediction)
        self.home_prediction.set(0)
        self.away_prediction = IntVar()
        self.away_prediction.trace("w",self.trace_away_prediction)
        self.away_prediction.set(0)
        
        self.extisting_prediction = self.check_if_record_exists()
    
    # def commit_predictions():
        
    def check_if_record_exists(self):
        result = DB_CURSOR.execute("SELECT PredictionAdded FROM '2023_24' WHERE HomeTeam = ? AND AwayTeam = ? and Player = ?",(self.hometeam,self.awayteam,self.player)).fetchall()
        return result[0][0] == 0
    
    def input_frame(self,master:Frame,master_row:int)->Frame:
        master.rowconfigure(master_row,weight=1)
        frame = Frame(master)
        home_label = Label(frame, text=self.hometeam,width=20,justify="right")
        home_label.grid(row=0,column=0,sticky="e")
        
        home_score_entry = ttk.Entry(frame,textvariable=self.home_prediction,width=5)
        home_score_entry.grid(row=0,column=1)
        
        dash = Label(frame,text=" - ",width=10)
        dash.grid(row=0,column=2)
        
        away_score_entry = ttk.Entry(frame,textvariable=self.away_prediction,width=5)
        away_score_entry.grid(row=0,column=3)
        
        away_label = Label(frame, text=self.awayteam,width=20,justify="left")
        away_label.grid(row=0,column=4,sticky="w")
        
        frame.grid(row=master_row)
    
    def trace_home_prediction(self,*args):
        if self.home_prediction.get() >= 0:
            self.isHomeValid = True
        else:
            self.isHomeValid = False
    
    def trace_away_prediction(self,*args):
        if self.away_prediction.get() >= 0:
            self.isAwayValid = True
        else:
            self.isAwayValid = False
    
    @property
    def AreInputsValid(self)->bool:
        return all([self.isHomeValid,self.isAwayValid])
    
    @property
    def db_values(self)->tuple:
        return(self.home_prediction.get(),self.away_prediction.get(),self.gameweek,1,self.hometeam,self.awayteam,self.player)
    
class AllGameweekPredictions():
    def __init__(self,fixture_data:list[FixtureData],player:str,master_frame:Frame,gameweek:str) -> None:
        self.all_rows = list()
        for row,fixture in enumerate(fixture_data):
            fixture_input = PredictionRow(player,gameweek,fixture)
            fixture_input.input_frame(master_frame,row)
            self.all_rows.append(fixture_input)
    
    def commit_predictions(self,table:str):
        
        self.check_scores()
        
        values = tuple([x.db_values for x in self.all_rows])
        
        DB_CURSOR.executemany(f"UPDATE '{table}' SET HomePrediction = ?, AwayPrediction = ?, Gameweek = ?, PredictionAdded = ? WHERE HomeTeam = ? AND AwayTeam = ? AND Player = ?",values)
        DB_CONNECTION.commit()
    
    def check_scores(self):
        if not all([x.AreInputsValid for x in self.all_rows]):
            messagebox.showerror("Incorrect Scores","Please Ensure all scores are valid")
        
class ManualPredictionInput():
    def __init__(self,master:Frame) -> None:
        
        # Create Frames
        self.index = LabelFrame(master,text="Index")
        self.inputs = LabelFrame(master,text="Predictions")
        self.buttons = LabelFrame(master,text="Buttons")
        
        # Weight Frames
        master.rowconfigure(0,weight=0)
        master.rowconfigure(1,weight=1)
        master.columnconfigure(0,weight=1)
        master.columnconfigure(1,weight=1)
        
        # Grid Frames
        self.index.grid(row=0,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.buttons.grid(row=0,column=1,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.inputs.grid(row=1,column=0,columnspan=2,sticky="nsew",padx=frame_padx,pady=frame_pady)
        
        #----------------------------------------------------------#
        #                       Index Section                      #
        #----------------------------------------------------------#
        
        # Frame Set Up
        self.index.columnconfigure(0,weight=1)
        self.index.columnconfigure(1,weight=1)
        self.player_frame = Frame(self.index)
        self.player_frame.grid(row=0,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.gw_frame = Frame(self.index)
        self.gw_frame.grid(row=0,column=1,sticky="nsew",padx=frame_padx,pady=frame_pady)
        
        self.player_label = Label(self.player_frame,text="Player:")
        self.player_label.grid(row=0,column=0,sticky="e")
        
        self.selected_player = StringVar()
        default_players = [x[0] for x in player_list()]
        default_players.insert(0,"Select Player")
        self.player_option = ttk.OptionMenu(self.player_frame,self.selected_player,*default_players)
        self.player_option.config(width=20)
        self.player_option.grid(row=0,column=1,sticky="w")
        
        self.gw_label = Label(self.gw_frame,text="Gameweek:")
        self.gw_label.grid(row=0,column=0,sticky="e")
        
        self.selected_gameweek = IntVar()
        self.selected_gameweek.set(1)
        self.gw_spinbox = ttk.Spinbox(self.gw_frame,textvariable=self.selected_gameweek,width=10, values=[str(x) for x in range(1,39)])
        self.gw_spinbox.grid(row=0,column=1,sticky="w")

        
        #-----------------------------------------------------------#
        #                       Button Section                      #
        #-----------------------------------------------------------#
        
        self.buttons.columnconfigure(0,weight=1)
        self.buttons.columnconfigure(1,weight=1)
        
        self.update_button = ttk.Button(self.buttons,text="Update Fixtures",width=30,command=self.update_prediction_fixtures)
        self.update_button.grid(row=0,column=0)
        
        self.commit_button = ttk.Button(self.buttons,text="Commit Predictions",width=30,command=self.commit_predictions)
        self.commit_button.grid(row=0,column=1)
    
    @property
    def gameweek(self)->int:
        return int(self.selected_gameweek.get())
    
    @property
    def player(self)->str:
        return str(self.selected_player.get())
        
    def update_prediction_fixtures(self,*args):
        if hasattr(self,"predictions"):
            clear_subframes(self.inputs)
            del self.predictions
        print("Update Fixture Button Pressed")
        self.generate_predictions()
        
    def commit_predictions(self,*args):
        print("Commit Fixture Button Pressed")
        if not hasattr(self,"predictions"):
            raise ValueError("No Prediction Object Yet!")
        self.predictions.commit_predictions("2023_24")
            
        
    def generate_predictions(self):
        
        # Fetch Gameweek Fixtures
        gw_data = get_gw_info(self.gameweek)
        
        self.inputs.columnconfigure(0,weight=1)
        
        self.predictions = AllGameweekPredictions(gw_data,self.player,self.inputs,self.gameweek)
            
        
        
        