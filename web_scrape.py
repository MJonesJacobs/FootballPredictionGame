import pandas as pd

GAMEWEEK = 37
WEBSITE  = f"https://fpl247.com/fixtures/game-week?weekId={GAMEWEEK}"

#Import Gameweek Fixtures from
webscrape_data = pd.read_html(WEBSITE)
print(webscrape_data)