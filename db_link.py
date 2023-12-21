from dataclasses import dataclass
import sqlite3
from web_scrape import FixtureData

DB_CONNECTION = sqlite3.connect('Prediction_Game.db')
DB_CURSOR = DB_CONNECTION.cursor()


def team_list(season:str)->list[str]:
    return [x[0] for x in DB_CURSOR.execute(f"SELECT DISTINCT HomeTeam FROM 'Results' WHERE Season = ?",(season,)).fetchall()]

def all_teams()->list[str]:
    "Returns all teams included in database"
    return [str(x) for x in DB_CURSOR.execute(f"""SELECT DISTINCT HomeTeam FROM 'Results' ORDER BY HomeTeam ASC""").fetchall()]

def season_teams(season:str)->list[str]:
    "Returns all teams for a specified season"
    return [x[0] for x in DB_CURSOR.execute(f"""SELECT DISTINCT HomeTeam FROM 'Results' WHERE season = ? ORDER BY HomeTeam ASC""",(season,)).fetchall()]

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

def player_list():
    player_list = DB_CURSOR.execute("SELECT * FROM 'Player List'").fetchall()
    return player_list

def all_seasons()->list[str]:
    season_list = [x[0] for x in DB_CURSOR.execute("SELECT Season from 'Season_Info'").fetchall()]
    return season_list

def current_gameweek(season:str)->[int,bool]:
    gws = [x[0] for x in DB_CURSOR.execute("SELECT DISTINCT Gameweek FROM 'Results' WHERE Season = ?",(season,)).fetchall()]    # Gets all gw's that have been added to database for season
    gws.remove(None)    #Drops Null values
    gws.sort()  # Sort lisr ascending order
    highest_gw = gws[-1]    # Get highest gw
    result_states = [x[0] for x in DB_CURSOR.execute("SELECT DISTINCT ResultAdded FROM 'Results' WHERE Season = ? AND Gameweek = ?",(season,highest_gw)).fetchall()] # Returns the states of the results will return [1] if all results added or [1,0] if partially

    if 0 in result_states:  # Having a 0 means that the gameweek results are not completed meaning it is the current gameweek
        return [highest_gw,True]
    else:   # All results are added in highes gw so next gameweek is current but nbot started yet
        return [highest_gw + 1,False]

CURRENT_SEASON = DB_CURSOR.execute("SELECT Season from 'Season_Info' WHERE Completed = 0").fetchone()[0]
print(f"{CURRENT_SEASON=}")

CURRENT_GAMEWEEK,PARTIAL_GAMEWEEKS = current_gameweek(season=CURRENT_SEASON)
print(f"{CURRENT_GAMEWEEK=}")
print(f"{PARTIAL_GAMEWEEKS=}")
