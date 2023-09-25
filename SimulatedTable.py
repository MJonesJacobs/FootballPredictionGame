# File to produce simulated Premier League table for all players

from db_link import DB_CURSOR, DB_CONNECTION
from tkinter import *
from tkinter import ttk
import pandas as pd
from copy import deepcopy


        
            

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
    actual_table = build_table(team_list,["Games Played","Points","GD"],[total_games,total_points,total_gd])    
    actual_table = actual_table.sort_values(by=["Points","GD"],ascending=False)
    actual_table["Actual Position"] = rank_position(actual_table["Team"].to_list())
    actual_table = actual_table.sort_values(by=["Team"])
    player_tables = {key:0 for key in players}
    
    
    for player in players:
        home_points = defualt_dict_update(count_home_points(season=season,player=player,result=False))
        away_points = defualt_dict_update(count_away_points(season=season,player=player,result=False))
        total_points = merge_dicts(home_points,away_points)
        home_gd = defualt_dict_update(count_home_gd(season=season,player=player,result=False))
        away_gd = defualt_dict_update(count_away_gd(season=season,player=player,result=False))
        total_gd = merge_dicts(home_gd,away_gd)
        
        player_table = build_table(team_list,[f"{player} Points",f"{player} GD"],[total_points,total_gd])
        player_table = player_table.sort_values(by=[f"{player} Points",f"{player} GD"],ascending=False)
        player_table[f"{player} Position"] = rank_position(player_table["Team"].to_list())
        player_table = player_table.sort_values(by=["Team"])
        player_table[f"{player} Difference"] = actual_table["Actual Position"]-player_table[f"{player} Position"]

        # number_cols = len(actual_table.columns)
        for col in [f"{player} Points",f"{player} GD",f"{player} Position",f"{player} Difference"]:
            actual_table[col] = player_table[col]
            
    return actual_table
            
class TableFrame():
    def __init__(self,master_frame:Frame) -> None:
        master_frame.rowconfigure(0,weight=1)
        master_frame.columnconfigure(0,weight=1)
        self.frame = master_frame
        
        table = predicted_table("2023_24",["Matt","Simon"])         
        
        table=table.sort_values(by=["Points","GD"],ascending=False)
        self.generate_treeview(table)
        
    def generate_treeview(self,table:pd.DataFrame):
        columns = table.columns.to_list()
        self.tree = ttk.Treeview(self.frame,show="headings", columns=columns)
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
        self.tree.tag_configure('evenrow', background='azure')
        self.tree.grid(row=0,column=0,sticky="nsew")