import pandas as pd


#Import Gameweek Fixtures from
def gameweek_url(gameweek:int)->str:
    return f"https://fpl247.com/fixtures/game-week?weekId={gameweek}"

def game_week_data(gameweek:int)->pd.DataFrame:
    return pd.read_html(gameweek_url(gameweek))[0]

def gameweek_fixtures(gameweek:int)->list[list[str]]:
    
    webscrape_data = game_week_data(gameweek)
    webscrape_data = webscrape_data[["Home","Away"]]
    webscrape_list = webscrape_data[["Home","Away"]].values.tolist()
    output_list = []
    for fixture in webscrape_list:
        fixture_short = []
        for team in fixture:
            fixture_short.append(team[:-5])
        output_list.append(fixture_short)
    return output_list


print(gameweek_fixtures(35))