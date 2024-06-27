from tkinter import *
from tkinter import ttk
from typing import Any
from db_link import player_list, current_gameweek, DB_CURSOR, DB_CONNECTION
from tkinter_functions import clear_subframes
from App_Formatting.formatting_conventions import frame_padx,frame_pady
from web_scrape import get_gw_info, FixtureData
from tkinter import messagebox
from TeamLogos import TeamImage
from team_names import convert_team_name

class PredictionRow():
    def __init__(self, player:str,gameweek:int, scape_data:FixtureData, row:int,season:str) -> None:
        self.row = row
        self.gameweek = gameweek
        self.player = player
        self.hometeam = convert_team_name(scape_data.home_team)
        self.awayteam = convert_team_name(scape_data.away_team)
        self.season = season
        self.home_prediction = IntVar()
        self.home_prediction.trace("w",self.trace_home_prediction)
        self.home_prediction.set(0)
        self.away_prediction = IntVar()
        self.away_prediction.trace("w",self.trace_away_prediction)
        self.away_prediction.set(0)
        
        self.extisting_prediction = self.check_if_record_exists()
    
    # def commit_predictions():
        
    def check_if_record_exists(self):
        result = DB_CURSOR.execute("SELECT PredictionAdded FROM 'Results' WHERE HomeTeam = ? AND AwayTeam = ? and Player = ? AND season = ?",(self.hometeam,self.awayteam,self.player,self.season)).fetchall()
        return result[0][0] == 1
    
    def get_existing_predictions(self):
        return DB_CURSOR.execute("SELECT HomePrediction, AwayPrediction FROM 'Results' WHERE HomeTeam = ? AND AwayTeam = ? and Player = ? AND season = ?",(self.hometeam,self.awayteam,self.player,self.season)).fetchall()[0]
    
    def input_frame(self,frame:Frame,master_row:int)->Frame:
        
        frame.rowconfigure(master_row,weight=1)
        
        self.home_logo = TeamImage(self.hometeam)
        self.home_logo_label = ttk.Label(frame,image=self.home_logo.photoimage,anchor=CENTER)
        self.home_logo_label.grid(row = self.row,column=1,sticky="nsew",padx=5,pady=5)
        home_label = Label(frame, text=self.hometeam,width=15,justify="right")
        home_label.grid(row = self.row,column=2,sticky="nsew",padx=5,pady=5)
        
        
        
        self.home_score_entry = ttk.Entry(frame,textvariable=self.home_prediction,width=5,justify=CENTER)
        self.home_score_entry.grid(row = self.row,column=3,padx=5,pady=5)
        
        dash = Label(frame,text=" - ",width=10)
        dash.grid(row = self.row,column=4,sticky="nsew",padx=5,pady=5)
        
        self.away_score_entry = ttk.Entry(frame,textvariable=self.away_prediction,width=5,justify=CENTER)
        self.away_score_entry.grid(row = self.row,column=5,padx=5,pady=5)
        
        away_label = Label(frame, text=self.awayteam,width=15,justify="left")
        away_label.grid(row = self.row,column=6,sticky="nsew",padx=5,pady=5)
        
        self.away_logo = TeamImage(self.awayteam)
        self.away_logo_label = ttk.Label(frame,image=self.away_logo.photoimage,anchor=CENTER)
        self.away_logo_label.grid(row = self.row,column=7,sticky="nsew",padx=5,pady=5)
        self.override = IntVar()
        self.override.trace("w",self.trace_override)
        self.override_check = ttk.Checkbutton(frame,text="Override:",var=self.override,compound=LEFT)
        self.override_check.grid(row = self.row,column=9,sticky="nsew",padx=5,pady=5)
        
        if self.extisting_prediction:
            home,away = self.get_existing_predictions()
            self.home_prediction.set(home)
            self.away_prediction.set(away)
            self.disable_entries()
            self.home_score_entry.config(state="disabled")
            self.away_score_entry.config(state="disabled")     
        else:
            self.override.set(1)
            self.override_check.config(state="disabled")   
        
    def trace_override(self,*args):
        if self.override.get() == 0:
            # Check disabled
            self.disable_entries()
        else:
            self.enable_entries()
            
    def enable_entries(self):
        self.home_score_entry.config(state="normal")
        self.away_score_entry.config(state="normal")
    
    def disable_entries(self):
        self.home_score_entry.config(state="disabled")
        self.away_score_entry.config(state="disabled")         
    
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
        return(self.home_prediction.get(),self.away_prediction.get(),self.gameweek,1,self.hometeam,self.awayteam,self.player,self.season)
    
class AllGameweekPredictions():
    def __init__(self,fixture_data:list[FixtureData],player:str,master_frame:Frame,gameweek:str,start_row:int,season:str) -> None:
        self.all_rows = list()
        for row,fixture in enumerate(fixture_data):
            fixture_input = PredictionRow(player,gameweek,fixture,start_row+row,season)
            fixture_input.input_frame(master_frame,start_row+row)
            self.all_rows.append(fixture_input)
    
    def commit_predictions(self):
        
        self.check_scores()
        
        values = tuple([x.db_values for x in self.override_active()])
        
        DB_CURSOR.executemany(f"UPDATE 'Results' SET HomePrediction = ?, AwayPrediction = ?, Gameweek = ?, PredictionAdded = ? WHERE HomeTeam = ? AND AwayTeam = ? AND Player = ? AND season = ?",values)
        DB_CONNECTION.commit()
    
    def check_scores(self):
        if not all([x.AreInputsValid for x in self.all_rows]):
            messagebox.showerror("Incorrect Scores","Please Ensure all scores are valid")
    
    def override_active(self)->list[FixtureData]:
        out = list()
        for fixture in self.all_rows:
            if fixture.override.get() == 1:
                out.append(fixture)
        return out
        
class ResultRow():
    def __init__(self, player:str,gameweek:int, scape_data:FixtureData, row:int,season:str) -> None:
        self.row = row
        self.gameweek = gameweek
        self.player = player
        self.hometeam = scape_data.home_team
        self.awayteam = scape_data.away_team
        self.season = season
        # self.home_prediction = IntVar()
        
        self.home_prediction, self.away_prediction = self.get_existing_predictions()
        self.home_result, self.away_result = self.get_existing_results()        
        self.extisting_prediction = self.check_if_result_Added()
        self.score = self.get_points()
        
    def check_if_result_Added(self):
        result = DB_CURSOR.execute("SELECT ResultAdded FROM 'Results' WHERE HomeTeam = ? AND AwayTeam = ? and Player = ? AND season = ?",(self.hometeam,self.awayteam,self.player,self.season)).fetchall()
        return result[0][0] == 1
    
    def get_existing_predictions(self):
        return DB_CURSOR.execute("SELECT HomePrediction, AwayPrediction FROM 'Results' WHERE HomeTeam = ? AND AwayTeam = ? and Player = ? AND season = ?",(self.hometeam,self.awayteam,self.player,self.season)).fetchall()[0]
    
    def get_existing_results(self):
        if self.check_if_result_Added():
            return DB_CURSOR.execute("SELECT HomeScore, AwayScore FROM 'Results' WHERE HomeTeam = ? AND AwayTeam = ? and Player = ? AND season = ?",(self.hometeam,self.awayteam,self.player,self.season)).fetchall()[0]
        else:
            return ("TBC","TBC")
        
    def get_points(self):
        if self.check_if_result_Added():
            return DB_CURSOR.execute("SELECT Points FROM 'Results' WHERE HomeTeam = ? AND AwayTeam = ? and Player = ? AND season = ?",(self.hometeam,self.awayteam,self.player,self.season)).fetchall()[0][0]
        else:
            return "NA"
        
    def input_frame(self,frame:Frame,master_row:int)->Frame:
        
        frame.rowconfigure(master_row,weight=1)
        
        self.home_logo = TeamImage(self.hometeam)
        self.home_logo_label = ttk.Label(frame,image=self.home_logo.photoimage,anchor=CENTER,width=10)
        self.home_logo_label.grid(row = self.row,column=1,sticky="nsew",padx=5,pady=5)
        home_label = Label(frame, text=self.hometeam,width=15,justify="right")
        home_label.grid(row = self.row,column=2,sticky="nsew",padx=5,pady=5)
        
        self.home_result_label = Label(frame,text=f"{self.home_result}",width=10) 
        self.home_result_label.grid(row = self.row,column=3,padx=5,pady=5)
        
        dash = Label(frame,text=" - ",width=5)
        dash.grid(row = self.row,column=4,sticky="nsew",padx=5,pady=5)
        
        self.away_result_label = Label(frame,text=f"{self.away_result}",width=10) 
        self.away_result_label.grid(row = self.row,column=5,padx=5,pady=5)
        
        away_label = Label(frame, text=self.awayteam,width=15,justify="left")
        away_label.grid(row = self.row,column=6,sticky="nsew",padx=5,pady=5)
        
        self.away_logo = TeamImage(self.awayteam)
        self.away_logo_label = ttk.Label(frame,image=self.away_logo.photoimage,anchor=CENTER,width=10)
        self.away_logo_label.grid(row = self.row,column=7,sticky="nsew",padx=5,pady=5)
        
        self.score_label = Label(frame, text=f"Score: {self.score}",width=15,justify="center")
        self.score_label.grid(row=self.row,column=9,sticky="nsew",padx=5,pady=5)
    
class AllGameweekResults():
    def __init__(self,fixture_data:list[FixtureData],player:str,master_frame:Frame,gameweek:str,start_row:int,season:str) -> None:
        self.all_rows = list()
        for row,fixture in enumerate(fixture_data):
            fixture_input = ResultRow(player,gameweek,fixture,start_row+row,season)
            fixture_input.input_frame(master_frame,start_row+row)
            self.all_rows.append(fixture_input)

class ManualPredictionInput():
    def __init__(self,master:Frame, season:str) -> None:
        self.season = season
        next_gw = current_gameweek(season)[0]
        # Create Frames
        self.index = LabelFrame(master,text="Index")
        self.predictions = LabelFrame(master,text="Predictions")
        self.result = LabelFrame(master,text="Result")
        self.buttons = LabelFrame(master,text="Buttons")
        
        # Weight Frames
        master.rowconfigure(0,weight=0)
        master.rowconfigure(1,weight=1)
        master.columnconfigure(0,weight=1)
        master.columnconfigure(1,weight=1)
        
        # Grid Frames
        self.index.grid(row=0,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.buttons.grid(row=0,column=1,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.predictions.grid(row=1,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.result.grid(row=1,column=1,sticky="nsew",padx=frame_padx,pady=frame_pady)
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
        default_players.insert(0,"")
        self.player_option = ttk.OptionMenu(self.player_frame,self.selected_player,*default_players)
        self.selected_player.set(default_players[1])
        self.player_option.config(width=20)
        self.player_option.grid(row=0,column=1,sticky="w")
        
        self.gw_label = Label(self.gw_frame,text="Gameweek:")
        self.gw_label.grid(row=0,column=0,sticky="e")
        
        self.selected_gameweek = IntVar()
        self.selected_gameweek.set(1)
        self.gw_spinbox = ttk.Spinbox(self.gw_frame,textvariable=self.selected_gameweek,width=10, from_=1, to=38,increment=1,wrap=True,)
        self.gw_spinbox.grid(row=0,column=1,sticky="w")
        
        self.selected_player.trace(mode="w",callback=self.update_prediction_fixtures)
        self.selected_gameweek.trace(mode="w",callback=self.update_prediction_fixtures)

        self.selected_gameweek.set(next_gw)
        
        #-----------------------------------------------------------#
        #                       Button Section                      #
        #-----------------------------------------------------------#
        
        self.buttons.columnconfigure(0,weight=1)
        self.buttons.columnconfigure(1,weight=1)
        
        # self.update_button = ttk.Button(self.buttons,text="Update Fixtures",width=30,command=self.update_prediction_fixtures)
        # self.update_button.grid(row=0,column=0)
        
        self.commit_button = ttk.Button(self.buttons,text="Commit Predictions",width=30,command=self.commit_predictions)
        self.commit_button.grid(row=0,column=1)
    
    @property
    def gameweek(self)->int:
        return int(self.selected_gameweek.get())
    
    @property
    def player(self)->str:
        return str(self.selected_player.get())
    
    def update_prediction_fixtures(self,*args):
        if hasattr(self,"prediction_row"):
            clear_subframes(self.predictions)
            clear_subframes(self.result)
            del self.prediction_row
            del self.result_row
            
        print("Update Fixture Button Pressed")
        self.generate_predictions()
        
    def commit_predictions(self,*args):
        print("Commit Fixture Button Pressed")
        if not hasattr(self,"prediction_row"):
            raise ValueError("No Prediction Object Yet!")
        self.prediction_row.commit_predictions()
        self.generate_predictions()
            
        
    def generate_predictions(self):
        
        # Fetch Gameweek Fixtures
        gw_data = get_gw_info(self.season,self.gameweek)
        
        # # Generate Frame Headers
        
        # home_header = Label(self.predictions,text="Home Team",anchor=CENTER)
        # home_header.grid(row=0,column=0,columnspan=2)
        
        # prediction_header = Label(self.predictions,text=f"{self.player} Prediction",anchor=CENTER)
        # prediction_header.grid(row=0,column=2,columnspan=3)
        
        # home_header = Label(self.predictions,text="Away Team",anchor=CENTER)
        # home_header.grid(row=0,column=5,columnspan=2)
        
        # edit_header = Label(self.predictions,text="Edit?",anchor=CENTER)
        # edit_header.grid(row=0,column=7)
        
        # header_sep = ttk.Separator(self.predictions,orient="horizontal")
        # header_sep.grid(row=1,column=0,columnspan=8,sticky="ew")

        # # for icol in 
        for frame in [self.predictions,self.result]:
            for col in [0,8,10]:
                frame.columnconfigure(col,weight=1)
        
        self.prediction_row = AllGameweekPredictions(gw_data,self.player,self.predictions,self.gameweek,0,season=self.season)
        self.result_row = AllGameweekResults(gw_data,self.player,self.result,self.gameweek,0,season=self.season)
        
        
        