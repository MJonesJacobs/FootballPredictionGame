import pandas as pd
from datetime import datetime
from dataclasses import dataclass
import re
from team_names import convert_team_name

SEASON_URL = {
    "23/24":'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
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

    def __post_init__(self):
        self.home_team = convert_team_name(self.home_team) # Update team name to correct format
        self.away_team = convert_team_name(self.away_team) # Update team name to correct format

    @property
    def db_values(self)->tuple:
        # UPDATE 'Results' SET HomeScore = ?, AwayScore = ?, Date = ?, ResultAdded = ?, Gameweek = ? WHERE HomeTeam = ? AND AwayTeam = ? AND season = ?"
        return (self.home_score,self.away_score,self.date,1,self.gameweek,self.home_team,self.away_team,self.season)    


#Import Gameweek Fixtures from
def gameweek_url(season:str)->str:
    if season == "23/24":
        # return f"https://fpl247.com/fixtures/game-week?weekId={gameweek}"
        return SEASON_URL[season]
    else:
        raise ValueError("No URL supported for input of non 23/24 season")

def game_week_data(season:str,gameweek:int)->pd.DataFrame:
    season_data = pd.read_html(gameweek_url(season=season))[0]
    gw_data = season_data[season_data["Wk"]==gameweek]
    return gw_data

def clean_name(name_str:str)->str:
    "Removes the abbreviation from the end of club name"
    return " ".join(name_str.split()[:-1])

def extract_score(score_str:str)->list[int,int]|None:
    if is_time(score_str):
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
                season=season
            )
        )
    return output_list

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