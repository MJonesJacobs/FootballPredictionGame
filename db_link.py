from dataclasses import dataclass
import sqlite3
from web_scrape import FixtureData

DB_CONNECTION = sqlite3.connect('Prediction_Game.db')
DB_CURSOR = DB_CONNECTION.cursor()

def team_list(season:str)->list[str]:
    return DB_CURSOR.execute(f"SELECT {season} FROM 'Team_List'").fetchall()

def all_teams(season:str)->list[str]:
    return [str(x[0]) for x in DB_CURSOR.execute(f"""SELECT DISTINCT HomeTeam FROM '{season}' ORDER BY HomeTeam ASC""").fetchall()]

def add_player(name:str,season:str):
    all_teams = team_list(season)
    db_push = list()
    for home in all_teams:
        for away in all_teams:
            if home == away:
                continue
            db_push.append(tuple([home[0],away[0],name]))
    DB_CURSOR.executemany("INSERT INTO '2023_24' (HomeTeam, AwayTeam, Player) VALUES (?,?,?)",db_push)
    DB_CONNECTION.commit()

def current_gameweek()->int:
    return DB_CURSOR.execute(f"SELECT DISTINCT Gameweek  FROM '2023_24' WHERE ResultAdded = 1 ORDER BY Gameweek DESC").fetchall()[0][0]+1      

def player_list():
    player_list = DB_CURSOR.execute("SELECT * FROM 'Player List'").fetchall()
    return player_list

print(current_gameweek())