from db_link import DB_CONNECTION, DB_CURSOR,CURRENT_SEASON, all_seasons
# from predication_emails import send_fixtures, read_predictions
from tkinter import ttk,LabelFrame,Tk, IntVar, StringVar, Label
import os
from App_Formatting.formatting_conventions import frame_padx,frame_pady
from tkinter_functions import clear_subframes
from manual_input import ManualPredictionInput
from SimulatedTable import TableFrame
from graphs import GraphFrame
from team_dashboard import TeamDashboard
from automatic_result_upload import update_results, update_scores, OverviewFrame

MAIN_DIR = os.getcwd()

class MainApp():
    def __init__(self) -> None:
        
        self.main_window = Tk()
        self.main_window.call("source",MAIN_DIR+r"\theme\azure.tcl")
        self.main_window.call("set_theme", "light")
        scrnwidth= self.main_window.winfo_screenwidth()
        scrnheight= self.main_window.winfo_screenheight()
        self.main_window.geometry("%dx%d" % (0.85*scrnwidth, 0.9*scrnheight))
        self.main_window.state('zoomed')


        scrnwidth= self.main_window.winfo_screenwidth()
        scrnheight= self.main_window.winfo_screenheight()

        self.main_window.columnconfigure(0,weight=0)
        self.main_window.columnconfigure(1,weight=1)
        self.main_window.rowconfigure(0,weight=0)
        self.main_window.rowconfigure(1,weight=0)
        self.main_window.rowconfigure(2,weight=1)

        self.season_frame = LabelFrame(self.main_window,text="Season",borderwidth=2)
        self.season_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=frame_padx,
            pady=frame_pady
        )      

        self.season_var = StringVar()
        season_values=all_seasons()
        season_label = Label(master=self.season_frame,text="Season:")
        season_label.grid(row=0,column=0,sticky="e",padx=frame_padx,pady=frame_pady)
        self.season_opt_menu = ttk.OptionMenu(self.season_frame,self.season_var,*season_values)
        self.season_var.set(CURRENT_SEASON)
        self.season_opt_menu.grid(row=0,column=1,sticky="w",padx=frame_padx,pady=frame_pady)
        self.season_var.trace("w",self.trace_season)

        self.radio_frame = LabelFrame(self.main_window,text="Radio Frame",borderwidth=2)

        self.radio_selection = IntVar()
        self.radio_selection.trace("w",self.trace_radio)
        # Main Menu
        self.radio_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=frame_padx,
            pady=frame_pady
        )      

        prediction_radio = ttk.Radiobutton(self.radio_frame, text="Prediction Input",variable=self.radio_selection,value=1)
        prediction_radio.grid(column=0,row=0,sticky="w",padx=frame_padx,pady=frame_pady)

        team_dashboard_radio = ttk.Radiobutton(self.radio_frame, text="Team Dashboard",variable=self.radio_selection,value=4)
        team_dashboard_radio.grid(column=0,row=1,sticky="w",padx=frame_padx,pady=frame_pady)
        
        simulated_table = ttk.Radiobutton(self.radio_frame, text="Simulated Table",variable=self.radio_selection,value=2)
        simulated_table.grid(column=0,row=2,sticky="w",padx=frame_padx,pady=frame_pady)
        
        graphs_radio = ttk.Radiobutton(self.radio_frame, text="Graphs",variable=self.radio_selection,value=3)
        graphs_radio.grid(column=0,row=3,sticky="w",padx=frame_padx,pady=frame_pady)

        self.overview = LabelFrame(self.main_window,text="Overview")
        self.overview.grid(row=2,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        
        self.season_var.set(CURRENT_SEASON)

        self.active_frame = LabelFrame(self.main_window,text="Active Frame",borderwidth=2,padx=frame_padx,pady=frame_pady)
        self.active_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=frame_padx,
            pady=frame_pady,
            rowspan=3
        )
        self.radio_selection.set(1) # Defaults to the prediction input

        # Start the main loop
        self.main_window.mainloop()
    
    @property
    def season(self)->str:
        return self.season_var.get()
    
    def generate_active_frame(self):
        self.active_frame = LabelFrame(self.main_window,text="Active Frame",borderwidth=2,padx=frame_padx,pady=frame_pady)
        self.active_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=frame_padx,
            pady=frame_pady,
            rowspan=3
        )
        
    def trace_season(self,*args):
        if hasattr(self,"overview_object"):
            clear_subframes(self.overview_object)
            del self.overview_object
        self.overview_object = OverviewFrame(self.overview,self.season)
        self.trace_radio()

    def trace_radio(self,*args):
        if hasattr(self,"active_frame"):
            clear_subframes(self.active_frame) # Clears whatever is in active frame
            self.generate_active_frame()
        
        if self.radio_selection.get() == 1:
            ManualPredictionInput(self.active_frame,season=self.season) # Initialises Prediction Frame
            
        if self.radio_selection.get() == 2:
            TableFrame(self.active_frame) # Initialises Table Frame
        
        if self.radio_selection.get() == 3:
            GraphFrame(self.active_frame)

        if self.radio_selection.get() == 4:
            TeamDashboard(self.active_frame,self.season)
            
            
           
if __name__ == "__main__":
    # Update any recent results;
    update_results(season=CURRENT_SEASON)
    print("Results Added")
    update_scores()
    print("Scores Updated")
    MainApp()

# read_predictions(38)