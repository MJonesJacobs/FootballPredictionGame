from web_scrape import get_gw_info, FixtureData
from db_link import DB_CURSOR, DB_CONNECTION

class Results():
    def __init__(self,results:list[FixtureData]) -> None:
        self.results = results
    
    def commit_data(self):
        values = tuple([x.db_values for x in self.results])
        DB_CURSOR.executemany("UPDATE '2023_24' SET HomeScore = ?, AwayScore = ?, Date = ?, ResultAdded = ? WHERE HomeTeam = ? AND AwayTeam = ?",values)
        DB_CONNECTION.commit()

fixture_data = get_gw_info(5)


missing_gws = [x[0] for x in DB_CURSOR.execute("SELECT gameweek FROM Data_Commits WHERE season = '2023_24' AND DataAdded = 0")]

all_fixtures = list()
for gw in missing_gws:
    data = get_gw_info(gw)
    if any([x.home_score == None for x in data]):
        break
    else:
        all_fixtures.extend(data)

results_to_add = Results(all_fixtures)
results_to_add.commit_data()