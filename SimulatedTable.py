# File to produce simulated Premier League table for all players

from db_link import DB_CURSOR, DB_CONNECTION
from tkinter import *
from tkinter import ttk
import pandas as pd
from copy import deepcopy
from App_Formatting.formatting_conventions import frame_padx, frame_pady
from tkinter_functions import clear_subframes

        
            

def build_table(row_indexes:list[str],column_names:list[dict],column_dicts:list[dict]):
    row_structure = list()
    for ii in range(len(column_dicts)):
        row_structure.append(list())
    
    for team in row_indexes:
        for i,col_dict in enumerate(column_dicts):
            row_structure[i].append(col_dict[team])
    df = pd.DataFrame()
    df["Team"] = row_indexes
    for i,name in enumerate(column_names):
        df[name] = row_structure[i]
    
    return df            

def merge_dicts(dict1:dict,dict2:dict):
    keys = set(dict1.keys())|set(dict2.keys())
    return {key:dict1[key]+dict2[key] for key in keys}

def count_home_games(season:str, player:str)->dict:
    return {key:value for key,value in DB_CURSOR.execute(f"""SELECT HomeTeam, COUNT(*) FROM '{season}' WHERE ResultAdded = 1 AND Player = ? GROUP BY HomeTeam ORDER BY HomeTeam ASC;""",(player,)).fetchall()}

def count_away_games(season:str, player:str)->dict:
    return {key:value for key,value in DB_CURSOR.execute(f"""SELECT AwayTeam, COUNT(*) FROM '{season}' WHERE ResultAdded = 1 AND Player = ? GROUP BY AwayTeam ORDER BY HomeTeam ASC;""",(player,)).fetchall()}

def count_home_points(season:str, player:str, result:bool= True)->dict:
    #Creat Temp Points Table
    suffix = "Score" if result == True else "Prediction"
    DB_CURSOR.execute(f"""
                      CREATE TEMPORARY TABLE point_data AS
    SELECT HomeTeam, Home{suffix}, Away{suffix}, 
    CASE                                              
        WHEN Home{suffix} > Away{suffix} THEN 3
        WHEN Home{suffix} = Away{suffix} THEN 1
        WHEN Home{suffix} < Away{suffix} THEN 0    
    END AS HomePoints
    FROM '{season}'
    WHERE Player = ? AND ResultAdded = 1;""",(player,))
    
    # Commit Temp Points Table
    DB_CONNECTION.commit()
    
     # Extract point Info
    result = DB_CURSOR.execute("""
    SELECT HomeTeam, IFNULL(SUM(HomePoints),0)
    FROM point_data
    GROUP BY HomeTeam;
    """).fetchall()
    
    DB_CURSOR.execute("""
    DROP TABLE point_data
    """)
    DB_CONNECTION.commit()
    print(result)
    
    return {key:value for key,value in result}

def count_away_points(season:str, player:str, result:bool= True)->dict:
    #Creat Temp Points Table
    suffix = "Score" if result == True else "Prediction"
    DB_CURSOR.execute(f"""
                      CREATE TEMPORARY TABLE point_data AS
    SELECT AwayTeam, Home{suffix}, Away{suffix}, 
    CASE                                              
        WHEN Away{suffix} > Home{suffix} THEN 3
        WHEN Away{suffix} = Home{suffix} THEN 1
        WHEN Away{suffix} < Home{suffix} THEN 0    
    END AS AwayPoints
    FROM '{season}'
    WHERE Player = ? AND ResultAdded = 1;""",(player,))
    
    # Commit Temp Points Table
    DB_CONNECTION.commit()
    
     # Extract point Info
    result = DB_CURSOR.execute("""
    SELECT AwayTeam, IFNULL(SUM(AwayPoints),0)
    FROM point_data
    GROUP BY AwayTeam;
    """).fetchall()
    
    DB_CURSOR.execute("""
    DROP TABLE point_data
    """)
    DB_CONNECTION.commit()
    print(result)
    
    return {key:value for key,value in result}

def count_home_gd(season:str, player:str, result:bool= True)->dict:
    #Creat Temp Points Table
    suffix = "Score" if result == True else "Prediction"
    DB_CURSOR.execute(f"""
                      CREATE TEMPORARY TABLE gd_data AS
    SELECT HomeTeam, Home{suffix}, Away{suffix}, (Home{suffix} - Away{suffix}) AS HomeGd
    FROM '{season}'
    WHERE Player = ? AND ResultAdded = 1;""",(player,))
    
    # Commit Temp Points Table
    DB_CONNECTION.commit()
    
     # Extract point Info
    result = DB_CURSOR.execute("""
    SELECT HomeTeam, IFNULL(SUM(HomeGd),0)
    FROM gd_data
    GROUP BY HomeTeam;
    """).fetchall()
    
    DB_CURSOR.execute("""
    DROP TABLE gd_data
    """)
    DB_CONNECTION.commit()
    print(result)
    
    return {key:value for key,value in result}

def count_away_gd(season:str, player:str, result:bool= True)->dict:
    #Creat Temp Points Table
    suffix = "Score" if result == True else "Prediction"
    DB_CURSOR.execute(f"""
                      CREATE TEMPORARY TABLE gd_data AS
    SELECT AwayTeam, Home{suffix}, Away{suffix}, (Away{suffix} - Home{suffix}) AS AwayGd
    FROM '{season}'
    WHERE Player = ? AND ResultAdded = 1;""",(player,))
    
    # Commit Temp Points Table
    DB_CONNECTION.commit()
    
     # Extract point Info
    result = DB_CURSOR.execute("""
    SELECT AwayTeam, IFNULL(SUM(AwayGd),0)
    FROM gd_data
    GROUP BY AwayTeam;
    """).fetchall()
    
    DB_CURSOR.execute("""
    DROP TABLE gd_data
    """)
    DB_CONNECTION.commit()
    print(result)
    
    return {key:value for key,value in result}
    

def all_teams(season:str)->list[str]:
    return [str(x[0]) for x in DB_CURSOR.execute(f"""SELECT DISTINCT HomeTeam FROM '{season}' ORDER BY HomeTeam ASC""").fetchall()]



def predicted_table(season:str,players:list[str])->pd.DataFrame:
    team_list = all_teams(season=season)
    team_dict = {key:0 for key in team_list}
    
    def defualt_dict_update(new_dict:dict):
        copy = deepcopy(team_dict)
        copy.update(new_dict)
        return copy
    
    def rank_position(ordered_list:list[str])->list[int]:
        return list(range(1,21))
            
    
    
    home_games = defualt_dict_update(count_home_games(season=season,player=players[0]))
    away_games = defualt_dict_update(count_away_games(season=season,player=players[0]))
    total_games = merge_dicts(home_games,away_games)
    home_points = defualt_dict_update(count_home_points(season=season,player=players[0]))
    away_points = defualt_dict_update(count_away_points(season=season,player=players[0]))
    total_points = merge_dicts(home_points,away_points)
    home_gd = defualt_dict_update(count_home_gd(season=season,player=players[0]))
    away_gd = defualt_dict_update(count_away_gd(season=season,player=players[0]))
    total_gd = merge_dicts(home_gd,away_gd)
    actual_table = build_table(team_list,["Played","Pts","Gd"],[total_games,total_points,total_gd])    
    actual_table = actual_table.sort_values(by=["Pts","Gd"],ascending=False)
    actual_table["Position"] = rank_position(actual_table["Team"].to_list())
    actual_table = actual_table.sort_values(by=["Team"])
    player_tables = {key:0 for key in players}
    
    
    for player in players:
        home_points = defualt_dict_update(count_home_points(season=season,player=player,result=False))
        away_points = defualt_dict_update(count_away_points(season=season,player=player,result=False))
        total_points = merge_dicts(home_points,away_points)
        home_gd = defualt_dict_update(count_home_gd(season=season,player=player,result=False))
        away_gd = defualt_dict_update(count_away_gd(season=season,player=player,result=False))
        total_gd = merge_dicts(home_gd,away_gd)
        
        player_table = build_table(team_list,[f"{player} Pts",f"{player} Gd"],[total_points,total_gd])
        player_table = player_table.sort_values(by=[f"{player} Pts",f"{player} Gd"],ascending=False)
        player_table[f"{player} Position"] = rank_position(player_table["Team"].to_list())
        player_table = player_table.sort_values(by=["Team"])
        player_table[f"{player} Diff"] = actual_table["Position"]-player_table[f"{player} Position"]

        # number_cols = len(actual_table.columns)
        for col in [f"{player} Pts",f"{player} Gd",f"{player} Position",f"{player} Diff"]:
            actual_table[col] = player_table[col]
            
    return actual_table
            
class TableFrame():
    sorting_options = ["Position","Matt Position","Matt Diff","Simon Position","Simon Diff"]
    def __init__(self,master_frame:Frame) -> None:
        master_frame.rowconfigure(0,weight=0)
        master_frame.rowconfigure(1,weight=1)
        master_frame.columnconfigure(0,weight=1)
        master_frame.columnconfigure(1,weight=0)
        
        self.table_frame = Frame(master_frame,padx=frame_padx, pady=frame_pady)
        self.table_frame.grid(column=0,row=0,rowspan=2,sticky="nsew")
        self.table_frame.rowconfigure(0,weight=1)
        self.table_frame.columnconfigure(0,weight=1)
        
        self.overview_frame = LabelFrame(master_frame,text="Overview",padx=frame_padx, pady=frame_pady)
        self.overview_frame.grid(column=1,row=1,sticky="nsew")
        
        self.sorting_frame = LabelFrame(master_frame,text="Table Editing",padx=frame_padx, pady=frame_pady)
        self.sorting_frame.grid(column=1,row=0,sticky="nsew")
        self.sorting_frame.columnconfigure(0,weight=1)
        
        self.table = predicted_table("2023_24",["Matt","Simon"])         
        
        self.table=self.table.sort_values(by=["Pts","Gd"],ascending=False)
        self.generate_treeview(self.table)
        self.generate_sorting_frame()
        self.generate_overview()
        
    def generate_treeview(self,table:pd.DataFrame):
        columns = table.columns.to_list()
        s = ttk.Style()
        s.configure('Treeview', rowheight=45)
        self.tree = ttk.Treeview(self.table_frame,show="headings", columns=columns)
        for i,col in enumerate(columns):
            self.tree.heading(col,text=col)
            self.tree.column(col,width=75,anchor=CENTER)
        # Iterate over the rows in the Pandas DataFrame and add each row to the Treeview widget
        for i in range(len(table)):
            if i % 2 == 0:
                self.tree.insert("", END, values=table.iloc[i,:].tolist(),tags= ('evenrow',))
            else:
                self.tree.insert("", END, values=table.iloc[i,:].tolist(),tags = ('oddrow',))
        self.tree.tag_configure('oddrow', background='white smoke')
        self.tree.tag_configure('evenrow', background='snow')
        self.tree.grid(row=0,column=0,sticky="nsew")
        
    def generate_sorting_frame(self):
        self.sort_option = StringVar()
        self.sort_option.set(self.sorting_options[0])
        
        for number,option in enumerate(self.sorting_options):
            radio_button = ttk.Radiobutton(self.sorting_frame, text=option, variable=self.sort_option, value=option)
            radio_button.grid(column=0,row=number, padx=frame_padx,pady=frame_pady,sticky="W")
            self.sorting_frame.rowconfigure(number,weight=0)
        
        self.sort_option.trace("w",self.trace_sort)
    
    def generate_overview(self):
        
        label = Label(self.overview_frame,text="Total Difference")
        label.grid(row=2,column=0)
        
        # Generate Names
        for i,player in enumerate(["Matt","Simon"]):
            name_label = Label(self.overview_frame,text=player)
            name_label.grid(row=0,column=i+1)
            
            total_score_label = Label(self.overview_frame,text=f"{self.difference_score(player)}")
            total_score_label.grid(row=2,column=i+1)
        
        # Seperators
        for row_num in [1,3]:
            sep = ttk.Separator(self.overview_frame,orient="horizontal")
            sep.grid(row=row_num,column=0,columnspan=3,sticky="ew",pady=5,padx=5)
        
        
        pass
    
    def difference_score(self,player:str):
        # Get the absolute value of each element in the column 'A'
        abs_difference = self.table[f'{player} Diff'].abs()

        # Calculate the sum of the absolute values
        sum_abs_A = abs_difference.sum()   
        return int(sum_abs_A)      
    
    def destroy_treeview(self):
        clear_subframes(self.table_frame)
    
    def trace_sort(self,*args):
        ascend_bool = True if any(x in self.sort_option.get() for x in ["Position","Diff"]) else False
        self.destroy_treeview()
        self.table = self.table.sort_values(by=self.sort_option.get(),ascending=ascend_bool)
        self.generate_treeview(self.table)
        print(self.sort_option.get())