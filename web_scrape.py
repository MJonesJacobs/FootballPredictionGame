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
    gameweek : int
    season :str
    
    @property
    def db_values(self)->tuple:
        # UPDATE 'Results' SET HomeScore = ?, AwayScore = ?, Date = ?, ResultAdded = ?, Gameweek = ? WHERE HomeTeam = ? AND AwayTeam = ? AND season = ?"
        return (self.home_score,self.away_score,self.date,1,self.gameweek,self.home_team,self.away_team,self.season)    


#Import Gameweek Fixtures from
def gameweek_url(season:str,gameweek:int)->str:
    if season == "23/24":
        return f"https://fpl247.com/fixtures/game-week?weekId={gameweek}"
    else:
        raise ValueError("No URL supported for input of non 23/24 season")

def game_week_data(season:str,gameweek:int)->pd.DataFrame:
    return pd.read_html(gameweek_url(season=season,gameweek=gameweek))[0]

def clean_name(name_str:str)->str:
    "Removes the abbreviation from the end of club name"
    return " ".join(name_str.split()[:-1])

def extract_score(score_str:str)->list[int,int]|None:
    if is_time(score_str):
        return [None,None]
    else:
        return [int(x) for x in score_str.split("-")]
    
def get_gw_info(season:str,gw_num:int)->list[FixtureData]:
    # Read data from website
    data_df = game_week_data(season=season,gameweek=gw_num)
    output_list = list()
    for _, row in data_df.iterrows():
        home_score, away_score = extract_score(row.iloc[3])            
        output_list.append(
            FixtureData(
                home_team=clean_name(row["Home"]),
                away_team=clean_name(row["Away"]),
                date=row["Date"],
                home_score=home_score,
                away_score=away_score,
                gameweek=gw_num,
                season=season
            )
        )
    return output_list