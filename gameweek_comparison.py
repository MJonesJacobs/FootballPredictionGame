from tkinter import ttk,LabelFrame,Tk, IntVar, StringVar, Label, Frame, CENTER
from db_link import player_list, CURRENT_GAMEWEEK
from App_Formatting.formatting_conventions import frame_padx,frame_pady
from web_scrape import get_gw_info, FixtureData
from TeamLogos import TeamImage
from tkinter_functions import clear_subframes

class ResultRow():
    def __init__(self,fixture:FixtureData) -> None:
        self.fixture_data = fixture
        
    def display_frame(self,master:Frame,row:int):

        
        self.home_logo = TeamImage(self.fixture_data.home_team)
        self.home_logo_label = ttk.Label(master,image=self.home_logo.photoimage,anchor=CENTER)
        self.home_logo_label.grid(row = row,column=1,sticky="nsew",padx=5,pady=5)
        
        home_label = Label(master, text=self.fixture_data.home_team,width=15,justify="right")
        home_label.grid(row = row,column=2,sticky="nsew",padx=5,pady=5)
        
        
        self.home_result_label = Label(master,text=f"{self.fixture_data.home_score}",width=10) 
        self.home_result_label.grid(row = row,column=3,padx=5,pady=5)
        
        dash = Label(master,text=" - ",width=5)
        dash.grid(row = row,column=4,sticky="nsew",padx=5,pady=5)
        
        self.away_result_label = Label(master,text=f"{self.fixture_data.away_score}",width=10) 
        self.away_result_label.grid(row = row,column=5,padx=5,pady=5)
        
        away_label = Label(master, text=self.fixture_data.away_team,width=15,justify="left")
        away_label.grid(row = row,column=6,sticky="nsew",padx=5,pady=5)
        
        self.away_logo = TeamImage(self.fixture_data.away_team)
        self.away_logo_label = ttk.Label(master,image=self.away_logo.photoimage,anchor=CENTER,width=10)
        self.away_logo_label.grid(row = row,column=7,sticky="nsew",padx=5,pady=5)

class GameweekComaparison():
    def __init__(self,master:Frame, season:str) -> None:
        self.season = season
        
        # Create Frames
        self.gw_select_Frame = Frame(master,bd=5)
        self.actual_scores_Frame = Frame(master,bd=5)
        self.player1_input_Frame = Frame(master,bd=5)
        self.player2_input_Frame = Frame(master,bd=5)
        self.player1_prediction_Frame = Frame(master,bd=5)
        self.player2_prediction_Frame = Frame(master,bd=5)
        
        # Weight Frames
        master.rowconfigure(0,weight=0)
        master.rowconfigure(1,weight=1)
        master.columnconfigure(0,weight=0)
        master.columnconfigure(1,weight=1)
        master.columnconfigure(2,weight=0)
        
        # Grid Frames
        self.gw_select_Frame.grid(row=0,column=1,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.player1_input_Frame.grid(row=0,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.player2_input_Frame.grid(row=0,column=2,sticky="nsew",padx=frame_padx,pady=frame_pady)

        self.actual_scores_Frame.grid(row=1,column=1,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.player1_prediction_Frame.grid(row=1,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        self.player2_prediction_Frame.grid(row=1,column=2,sticky="nsew",padx=frame_padx,pady=frame_pady)
       
        # INPUT VARIABLE CREATION

        # GW Int

        Label(self.gw_select_Frame,text="Gameweek:",width=15,justify="right").grid(column=0,row=0)
        self.selected_gameweek = IntVar()
        self.gw_spinbox = ttk.Spinbox(self.gw_select_Frame,textvariable=self.selected_gameweek,width=10, from_=1, to=38,increment=1,wrap=True)
        self.gw_spinbox.grid(row=0,column=1)
        self.selected_gameweek.set(CURRENT_GAMEWEEK)
        self.selected_gameweek.trace_add(mode="write",callback=self.trace_GW)

        # Player 1
        Label(self.player1_input_Frame,text="Player:",width=15,justify="right").grid(column=0,row=0)
        self.player1 = StringVar()
        default_players = [x[0] for x in player_list()]
        default_players.insert(0,"")
        self.player1_option = ttk.OptionMenu(self.player1_input_Frame,self.player1,*default_players)
        self.player1_option.config(width=20)
        self.player1_option.grid(row=0,column=1,sticky="w")
        self.player1.set(default_players[1])
        self.player1.trace_add(mode="write",callback=self.trace_player1)
        
        Label(self.player2_input_Frame,text="Player:",width=15,justify="right").grid(column=0,row=0)
        self.player2 = StringVar()
        self.player2_option = ttk.OptionMenu(self.player2_input_Frame,self.player2,*default_players)
        self.player2_option.config(width=20)
        self.player2_option.grid(row=0,column=1,sticky="w")
        self.player2.set(default_players[2])
        self.player2.trace_add(mode="write",callback=self.trace_player2)

        self.generate_gw_results()

    def generate_gw_results(self):
        "Generates the list of results with team name, logos and result to be shown in actual score frame"
        clear_subframes(self.actual_scores_Frame)

        # Retrieve Scores

        gw_data = get_gw_info(self.season,self.selected_gameweek.get())
        self.rows = list()
        for i,fixture in enumerate(gw_data):
            self.actual_scores_Frame.rowconfigure(i,weight=1)
            game = ResultRow(fixture)
            self.rows.append(game)
            game.display_frame(self.actual_scores_Frame,i)

    def trace_GW(self,*args):
        # Update Results
        print("Gameweek Updated - New Results Added")

        self.generate_gw_results()
        # Update Player Predictions
        self.trace_player1()
        self.trace_player2()

    def trace_player1(self,*args):
        print("player1 prediction update")

    def trace_player2(self,*args):
        print("player2 prediction update")

    # gw_data = get_gw_info(self.season,self.gameweek)
        
    #     # Frame Set Up
    #     self.index.columnconfigure(0,weight=1)
    #     self.index.columnconfigure(1,weight=1)
    #     self.player_frame = Frame(self.index)
    #     self.player_frame.grid(row=0,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
    #     self.gw_frame = Frame(self.index)
    #     self.gw_frame.grid(row=0,column=1,sticky="nsew",padx=frame_padx,pady=frame_pady)
        
    #     self.player_label = Label(self.player_frame,text="Player:")
    #     self.player_label.grid(row=0,column=0,sticky="e")
        
    #     self.selected_player = StringVar()
    #     default_players = [x[0] for x in player_list()]
    #     default_players.insert(0,"")
    #     self.player_option = ttk.OptionMenu(self.player_frame,self.selected_player,*default_players)
    #     self.selected_player.set(default_players[1])
    #     self.player_option.config(width=20)
    #     self.player_option.grid(row=0,column=1,sticky="w")
        
    #     self.gw_label = Label(self.gw_frame,text="Gameweek:")
    #     self.gw_label.grid(row=0,column=0,sticky="e")
        
    #     self.selected_gameweek = IntVar()
    #     self.selected_gameweek.set(1)
    #     self.gw_spinbox = ttk.Spinbox(self.gw_frame,textvariable=self.selected_gameweek,width=10, from_=1, to=38,increment=1,wrap=True,)
    #     self.gw_spinbox.grid(row=0,column=1,sticky="w")
        
    #     self.selected_player.trace(mode="w",callback=self.update_prediction_fixtures)
    #     self.selected_gameweek.trace(mode="w",callback=self.update_prediction_fixtures)

    #     self.selected_gameweek.set(next_gw)
        
    #     #-----------------------------------------------------------#
    #     #                       Button Section                      #
    #     #-----------------------------------------------------------#
        
    #     self.buttons.columnconfigure(0,weight=1)
    #     self.buttons.columnconfigure(1,weight=1)
        
    #     # self.update_button = ttk.Button(self.buttons,text="Update Fixtures",width=30,command=self.update_prediction_fixtures)
    #     # self.update_button.grid(row=0,column=0)
        
    #     self.commit_button = ttk.Button(self.buttons,text="Commit Predictions",width=30,command=self.commit_predictions)
    #     self.commit_button.grid(row=0,column=1)
    
    # @property
    # def gameweek(self)->int:
    #     return int(self.selected_gameweek.get())
    
    # @property
    # def player(self)->str:
    #     return str(self.selected_player.get())
    
    # def update_prediction_fixtures(self,*args):
    #     if hasattr(self,"prediction_row"):
    #         clear_subframes(self.predictions)
    #         clear_subframes(self.result)
    #         del self.prediction_row
    #         del self.result_row
            
    #     print("Update Fixture Button Pressed")
    #     self.generate_predictions()
        
    # def commit_predictions(self,*args):
    #     print("Commit Fixture Button Pressed")
    #     if not hasattr(self,"prediction_row"):
    #         raise ValueError("No Prediction Object Yet!")
    #     self.prediction_row.commit_predictions()
    #     self.generate_predictions()