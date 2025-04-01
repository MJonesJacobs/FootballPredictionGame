import pandas as pd
from datetime import datetime
from dataclasses import dataclass
import re
from team_names import convert_team_name
from typing import Literal
SEASON_URL = {
    "23/24":'https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures',
    "24/25":'https://fbref.com/en/comps/9/2024-2025/schedule/2024-2025-Premier-League-Scores-and-Fixtures'
}



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
    time : str

    def __post_init__(self):
        self.home_team = convert_team_name(self.home_team) # Update team name to correct format
        self.away_team = convert_team_name(self.away_team) # Update team name to correct format
    
    def __hash__(self) -> int:
        return hash(tuple([self.home_team,self.away_team,self.season]))
    
    def fixture_str(self) -> str:
        return f"{self.home_team} - {self.away_team}"
    
    def result_str(self)-> str:
        return f"{self.home_team} {self.home_score} - {self.away_score} {self.away_team}"

    @property
    def db_values(self)->tuple:
        # UPDATE 'Results' SET HomeScore = ?, AwayScore = ?, Date = ?, ResultAdded = ?, Gameweek = ? WHERE HomeTeam = ? AND AwayTeam = ? AND season = ?"
        return (self.home_score,self.away_score,self.date,1,self.gameweek,self.home_team,self.away_team,self.season)    


#Import Gameweek Fixtures from
def gameweek_url(season:str)->str:
    try:
        return SEASON_URL[season]
    except:
        raise ValueError("No URL supported for input of non 23/24 season")

def game_week_data(season:str,gameweek:int)->pd.DataFrame:
    season_data = pd.read_html(gameweek_url(season=season))[0]
    gw_data = season_data[season_data["Wk"]==gameweek]
    if "Notes" in gw_data.columns: # Additional Dlag to filter out Postponed games
        gw_data = gw_data[gw_data['Notes']!='Match Postponed']
        # Need to add in code to delete these from DB when detected
    return gw_data

def clean_name(name_str:str)->str:
    "Removes the abbreviation from the end of club name"
    return " ".join(name_str.split()[:-1])

def extract_score(score_str:str)->list[int,int]|None:
    if pd.isna(score_str):
        return [None,None]
    else:
        return [int(x) for x in score_str.split("–")]

def date_format(date_string:str)->str:
    "Formats date provided into DD/MM/YYYY format"
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")
    
def get_gw_info(season:str,gw_num:int)->list[FixtureData]:
    # Read data from website
    data_df = game_week_data(season=season,gameweek=gw_num)
    output_list = list()
    for _, row in data_df.iterrows():
        home_score, away_score = extract_score(row["Score"])         
        output_list.append(
            FixtureData(
                home_team=row["Home"],
                away_team=row["Away"],
                date=date_format(row["Date"]),
                home_score=home_score,
                away_score=away_score,
                gameweek=gw_num,
                season=season,
                time=row["Time"]
            )
        )
    sorted_list = sorted(output_list, key = lambda x:(datetime.strptime(x.date, '%d/%m/%Y'),x.time,x.home_team))
    return sorted_list


class GameweekFixtures():
    def __init__(self,season:Literal["23/24","24/25"],gw:int) -> None:
        self.season = season
        self.gw = gw
        self.fixtures = get_gw_info(season=season,gw_num=gw)

if __name__ == '__main__':

    # GW = 38
    # SEASON = "2023/24"
    # data = pd.read_html('https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures')[0]
    # gw_data_df = data[data["Wk"]==GW]
    # output_list = list()
    # for _,row in gw_data_df.iterrows():
    #     home_score, away_score = extract_score(row["Score"])            
    #     output_list.append(
    #         FixtureData(
    #             home_team=row["Home"],
    #             away_team=row["Away"],
    #             date=date_format(row["Date"]),
    #             home_score=home_score,
    #             away_score=away_score,
    #             gameweek=row["Wk"],
    #             season=SEASON
    #         )
    #     )
    pass