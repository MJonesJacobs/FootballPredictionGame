from dataclasses import dataclass
import sqlite3
from web_scrape import FixtureData

DB_CONNECTION = sqlite3.connect('Prediction_Game.db')
DB_CURSOR = DB_CONNECTION.cursor()
CURRENT_SEASON = "23/24"
SEASON_LIST = ["23/24"]

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

def current_gameweek(season:str)->[int,bool]:
    gws = [x[0] for x in DB_CURSOR.execute("SELECT DISTINCT Gameweek FROM 'Results' WHERE Season = ?",(season,)).fetchall()]    # Gets all gw's that have been added to database for season
    if None in gws:
        gws.remove(None)    #Drops Null values
    gws.sort()  # Sort lisr ascending order
    highest_gw = gws[-1]    # Get highest gw
    result_states = [x[0] for x in DB_CURSOR.execute("SELECT DISTINCT ResultAdded FROM 'Results' WHERE Season = ? AND Gameweek = ?",(season,highest_gw)).fetchall()] # Returns the states of the results will return [1] if all results added or [1,0] if partially

    if 0 in result_states:  # Having a 0 means that the gameweek results are not completed meaning it is the current gameweek
        return [highest_gw,True]
    else:   # All results are added in highes gw so next gameweek is current but nbot started yet maximum gameweek number is 39
        return [min(highest_gw + 1,38),False]

def initiate_new_season(season:str,team_list:list[str],player_list:list[str]):
    """
    CAUTION - METHOD ALTERS DB SO ENSURE BACK UP BEFORE USE
    
    Populate DB with team fixtures names, player and season ready for new season
    """
    db_push = list()
    for name in player_list:  
        for home in team_list:
            for away in team_list:
                if home == away:
                    continue # Avoids team facing itself
                db_push.append(tuple([home,away,name,season]))
    DB_CURSOR.executemany("INSERT INTO 'Results' (HomeTeam, AwayTeam, Player, Season) VALUES (?,?,?,?)",db_push)
    DB_CONNECTION.commit()

# DEFINES GLOBAL VARIABLES at Main.py Import
CURRENT_GAMEWEEK,PARTIAL_GAMEWEEKS = current_gameweek(season=CURRENT_SEASON)
print(f"{CURRENT_GAMEWEEK=}")
print(f"{PARTIAL_GAMEWEEKS=}")

# if __name__ == "__main__":
    # initiate_new_season(
    #     season="24/25",
    #     team_list=[
    #         "Fulham",
    #         "Brentford",
    #         "Liverpool",
    #         "Bournemouth",
    #         "Wolves",
    #         "Brighton",
    #         "Spurs",
    #         "Man Utd",
    #         "Man City",
    #         "Newcastle",
    #         "Aston Villa",
    #         "Everton",
    #         "West Ham",
    #         "Chelsea",
    #         "Crystal Palace",
    #         "Arsenal",
    #         "Burnley",
    #         "Ipswich Town",
    #         "Leicester City",
    #         "Southampton"],
    #     player_list=[
    #         "Matt",
    #         "Simon"
    #     ])
