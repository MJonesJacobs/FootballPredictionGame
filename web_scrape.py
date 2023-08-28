import pandas as pd
from dataclasses import dataclass
import re

def is_time(string):
    regex = r'^([0-2]?[0-9]:[0-5][0-9])$'
    match = re.match(regex, string)
    return match is not None

@dataclass
class FixtureData():
    home_team : str
    home_score : int | None
    away_team : str
    away_score : int | None
    date : str
    
    @property
    def db_values(self)->tuple:
        return (self.home_score,self.away_score,self.date,1,self.home_team,self.away_team)
    


#Import Gameweek Fixtures from
def gameweek_url(gameweek:int)->str:
    return f"https://fpl247.com/fixtures/game-week?weekId={gameweek}"

def game_week_data(gameweek:int)->pd.DataFrame:
    return pd.read_html(gameweek_url(gameweek))[0]

def clean_name(name_str:str)->str:
    "Removes the abbreviation from the end of club name"
    return " ".join(name_str.split()[:-1])

def extract_score(score_str:str)->list[int,int]|None:
    if is_time(score_str):
        return [None,None]
    else:
        return [int(x) for x in score_str.split("-")]
    
def get_gw_info(gw_num:int)->list[FixtureData]:
    # Read data from website
    data_df = game_week_data(gameweek=gw_num)
    output_list = list()
    for _, row in data_df.iterrows():
        home_score, away_score = extract_score(row.iloc[3])            
        output_list.append(
            FixtureData(
                home_team=clean_name(row["Home"]),
                away_team=clean_name(row["Away"]),
                date=row["Date"],
                home_score=home_score,
                away_score=away_score
            )
        )
    return output_list