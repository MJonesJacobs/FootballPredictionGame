from web_scrape import get_gw_info, FixtureData
from db_link import DB_CURSOR, DB_CONNECTION

class Results():
    def __init__(self,results:list[FixtureData],new_gws:list[int]) -> None:
        self.results = results
        self.new_gws = tuple(new_gws)
    
    def commit_data(self):
        values = tuple([x.db_values for x in self.results])
        DB_CURSOR.executemany("UPDATE '2023_24' SET HomeScore = ?, AwayScore = ?, Date = ?, ResultAdded = ? WHERE HomeTeam = ? AND AwayTeam = ?",values)
        DB_CONNECTION.commit()
        DB_CURSOR.executemany("UPDATE 'Data_Commits' SET  DataAdded = 1 WHERE season = '2023_24' AND gameweek = ?",self.new_gws )
        DB_CONNECTION.commit()
        

def update_results():
    missing_gws = [x[0] for x in DB_CURSOR.execute("SELECT gameweek FROM Data_Commits WHERE season = '2023_24' AND DataAdded = 0")]

    gws_to_add = list()
    all_fixtures = list()
    for gw in missing_gws:
        data = get_gw_info(gw)
        
        if any([x.home_score == None for x in data]):
            break
        else:
            all_fixtures.extend(data)
            gw_tuple = (gw,)
            gws_to_add.append(gw_tuple)

    results_to_add = Results(all_fixtures,gws_to_add)
    results_to_add.commit_data()

def update_scores():
    DB_CURSOR.execute("""
UPDATE '2023_24'
SET Points =
    CASE
        WHEN HomeScore = HomePrediction AND AwayScore = AwayPrediction THEN 3
        WHEN sign(HomeScore - AwayScore) = sign(HomePrediction - AwayPrediction) THEN 1
        ELSE 0
    END
WHERE PredictionAdded = 1 AND ResultAdded = 1;
""")
    DB_CONNECTION.commit()

update_scores()