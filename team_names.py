"This file contains methods and variables used to format team names to a standardised naming convention"

# Team Names are defined here
DB_TEAM_NAMES = ["Nott'm Forest",
                 "Sheffield Utd",
                 "Fulham",
                 "Brentford",
                 "Liverpool",
                 "Bournemouth",
                 "Wolves",
                 "Brighton",
                 "Spurs",
                 "Man Utd",
                 "Man City",
                 "Newcastle",
                 "Aston Villa",
                 "Everton",
                 "West Ham",
                 "Chelsea",
                 "Crystal Palace",
                 "Arsenal",
                 "Burnley",
                 "Luton",
                 "Ipswich Town",
                 "Leicester City",
                 "Southampton"]

KNOWN_TRANSLATIONS = {
    "Nott'ham Forest":"Nott'm Forest",
    "Manchester City":"Man City",
    "Luton Town":"Luton",
    "Newcastle Utd":"Newcastle",
    "Manchester Utd":"Man Utd",
    "Tottenham":"Spurs"
}

def convert_team_name(team_str:str):
    "Returns the team name from web scrape in DB form to keep team names consistent within DB"
    if team_str in DB_TEAM_NAMES: # Checks if name is already in correct format
        return team_str
    try:
        return KNOWN_TRANSLATIONS[team_str] 
    except KeyError:
        raise "Invalid Team Name"