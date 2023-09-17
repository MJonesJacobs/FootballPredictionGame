
import db_link
from predication_emails import send_fixtures, read_predictions
from tkinter import ttk,LabelFrame,Tk, IntVar
import os
from App_Formatting.formatting_conventions import frame_padx,frame_pady
from tkinter_functions import clear_subframes
from manual_input import ManualPredictionInput
from SimulatedTable import TableFrame
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
        self.main_window.rowconfigure(1,weight=1)

        self.radio_frame = LabelFrame(self.main_window,text="Radio Frame",borderwidth=2)

        self.radio_selection = IntVar()
        self.radio_selection.trace("w",self.trace_radio)
        # Main Menu
        self.radio_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=frame_padx,
            pady=frame_pady
        )      
        

        prediction_radio = ttk.Radiobutton(self.radio_frame, text="Prediction Input",variable=self.radio_selection,value=1)
        prediction_radio.grid(column=0,row=0,sticky="w")
        simulated_table = ttk.Radiobutton(self.radio_frame, text="Simulated Table",variable=self.radio_selection,value=2)
        simulated_table.grid(column=0,row=1,sticky="w")

        self.overview = LabelFrame(self.main_window,text="Overview")
        self.overview.grid(row=1,column=0,sticky="nsew",padx=frame_padx,pady=frame_pady)
        overview_object = OverviewFrame(self.overview)

        self.active_frame = LabelFrame(self.main_window,text="Active Frame",borderwidth=2)
        self.active_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=frame_padx,
            pady=frame_pady,
            rowspan=2
        )


        # Start the main loop
        self.main_window.mainloop()
        
        
    def trace_radio(self,*args):
        print(f"{self.radio_selection.get()}")
        clear_subframes(self.active_frame) # Clears whatever is in active frame
        if self.radio_selection.get() == 1:
            ManualPredictionInput(self.active_frame) # Initialises Prediction Frame
        if self.radio_selection.get() == 2:
            TableFrame(self.active_frame)
            
            
           
if __name__ == "__main__":
    # Update any recent results;
    update_results()
    print("Results Added")
    update_scores()
    print("Scores Updated")
    MainApp()

# read_predictions(38)