from web_scrape import get_gw_info, FixtureData
from db_link import DB_CURSOR, DB_CONNECTION, CURRENT_SEASON
from tkinter import *
from tkinter import ttk

class Results():
    def __init__(self,results:list[FixtureData],season:str) -> None:
        self.results = results
        self.season = season
        # self.new_gws = tuple(new_gws)
    
    def commit_data(self):
        values = tuple([x.db_values for x in self.results])
        DB_CURSOR.executemany("UPDATE 'Results' SET HomeScore = ?, AwayScore = ?, Date = ?, ResultAdded = ?, Gameweek = ?  WHERE HomeTeam = ? AND AwayTeam = ? AND season = ?",values)
        DB_CONNECTION.commit()
        # # CHeck if all values of
        # DB_CURSOR.executemany("UPDATE 'Data_Commits' SET  DataAdded = 1 WHERE season = 'Results' AND gameweek = ?",self.new_gws )
        # DB_CONNECTION.commit()
        
def total_score(season:str,player:str)->int:
    return DB_CURSOR.execute("SELECT SUM(Points) FROM 'Results' WHERE season = ? AND player = ?",(season,player)).fetchone()[0]

def gw_score(season:str,player:str,gw:int)->int:
    return DB_CURSOR.execute("SELECT SUM(Points) FROM 'Results' WHERE season = ? AND player = ? AND gameweek = ?",(season,player,gw)).fetchone()[0]

def total_score_upto_gw(season:str,player:str,gw:int):
    return DB_CURSOR.execute("SELECT SUM(Points) FROM 'Results' WHERE season = ? AND player = ? AND gameweek <= ? AND ResultAdded = 1",(season,player,gw)).fetchone()[0]

def top_home_teams(season:str,player:str):
    return DB_CURSOR.execute("SELECT HomeTeam ,SUM(points) AS Points FROM 'Results' WHERE season = ? AND player = ? AND ResultAdded = 1 GROUP BY HomeTeam ORDER BY Points DESC, HomeTeam ASC",(season,player)).fetchall()

def top_away_teams(season:str,player:str):
    return DB_CURSOR.execute("SELECT AwayTeam ,SUM(points) AS Points FROM 'Results' WHERE season = ? AND player = ? AND ResultAdded = 1 GROUP BY AwayTeam ORDER BY Points DESC, AwayTeam ASC",(season,player)).fetchall()

def number_points(season:str,player:str,point:int):
    return DB_CURSOR.execute("SELECT COUNT(Points) FROM 'Results' WHERE season = ? AND player = ? AND Points = ? AND ResultAdded = 1",(season,player,point)).fetchone()[0]
    
def update_results(season:str):
    # Get all gameweeks with missing resuts
    gameweeks = set(range(1,39))
    missing_gws = list(set([x[0] for x in DB_CURSOR.execute("SELECT DISTINCT Gameweek FROM 'Results' WHERE season = ? AND ResultAdded = 0",(season,)).fetchall()]))
    missing_gws.remove(None)
    missing_gws.sort()

    gws_to_add = list()
    all_fixtures = list()
    complete_gws = list()
    for gw in missing_gws:
        data = get_gw_info(season=season,gw_num=gw)
        
        if all([x.home_score == None for x in data]):
            break #Ignores unplayed gameweeks
        else:
            for result in data:
                if result.home_score != None:
                    all_fixtures.append(result)
                    gws_to_add.append(gw)
            
            # if len(data)==len(all_fixtures):
            #     gws_to_add.append((gw,))
                
                    
            # gw_tuple = (gw,)
            # gws_to_add.append(gw_tuple)

    results_to_add = Results(all_fixtures,gws_to_add)
    results_to_add.commit_data()

def update_scores():
    DB_CURSOR.execute("""
UPDATE 'Results'
SET Points =
    CASE
        WHEN HomeScore = HomePrediction AND AwayScore = AwayPrediction THEN 3
        WHEN sign(HomeScore - AwayScore) = sign(HomePrediction - AwayPrediction) THEN 1
        ELSE 0
    END
WHERE PredictionAdded = 1 AND ResultAdded = 1;
""")
    DB_CONNECTION.commit()


class OverviewFrame():
    def __init__(self,master:Frame,season:str) -> None:
        self.season = season
        for row in range(31):
            master.rowconfigure(row,weight=1)
        
        total_label = Label(master,text="Total Score",justify="center",padx=5,pady=2)
        total_label.grid(row=2,column=0) 
        
        sep = ttk.Separator(master,orient="horizontal")
        sep.grid(row=1,column=0,columnspan=3,sticky="ew",pady=5,padx=5)
        
        sep = ttk.Separator(master,orient="horizontal")
        sep.grid(row=3,column=0,columnspan=3,sticky="ew",pady=5,padx=5)
        
        sep = ttk.Separator(master,orient="horizontal")
        sep.grid(row=9,column=0,columnspan=3,sticky="ew",pady=5,padx=5)
        
        sep = ttk.Separator(master,orient="horizontal")
        sep.grid(row=15,column=0,columnspan=3,sticky="ew",pady=5,padx=5)
        
        sep = ttk.Separator(master,orient="horizontal")
        sep.grid(row=19,column=0,columnspan=3,sticky="ew",pady=5,padx=5)
        
        sep = ttk.Separator(master,orient="horizontal")
        sep.grid(row=25,column=0,columnspan=3,sticky="ew",pady=5,padx=5)
        
        for i,gw in enumerate(self.recent_gameweeks(self.season)):
            lab = Label(master,text=f"Gameweek {gw}",justify="left",padx=5,pady=2)
            lab.grid(row=i+4,column=0)
            
            lab = Label(master,text=f"Gameweek {gw}",justify="left",padx=5,pady=2)
            lab.grid(row=i+10,column=0)
        
        for ii,name in enumerate(["Matt","Simon"]):
            home_top = top_home_teams(self.season,name)
            away_top = top_away_teams(self.season,name)
            
            name_label = Label(master,text=name,justify="center",padx=5,pady=2)
            name_label.grid(row=0,column=ii+1)
            
            total_score_str = total_score(self.season,name) 
            total_score_label = Label(master,text=total_score_str,justify="center",padx=2,pady=2)
            total_score_label.grid(row=2,column=ii+1)

            for i,gw in enumerate(self.recent_gameweeks(self.season)):
                score = gw_score(self.season,name,gw)
                score_label = Label(master,text=str(score),justify="center",padx=5,pady=2)
                score_label.grid(row=i+4,column=ii+1)
                
                cumulative_score = total_score_upto_gw(self.season,name,gw)
                cumulative_score_label = Label(master,text=str(cumulative_score),justify="center",padx=5,pady=2)
                cumulative_score_label.grid(row=i+10,column=ii+1)
        
            for i,point in enumerate([3,1,0]):
                lab = Label(master,text=f"{point} Point Games",justify="left",padx=5,pady=2)
                lab.grid(column=0,row=16+i)
                
                point_total = number_points(self.season,name,point)
                point_label = Label(master,text=str(point_total),justify="center",padx=5,pady=2)
                point_label.grid(row=i+16,column=ii+1)
            
            for i in range(5):
                lab = Label(master,text=f"Home Rank {i+1}")
                lab.grid(column=0,row=20+i)
                lab = Label(master,text=f"Away Rank {i+1}")
                lab.grid(column=0,row=26+i)
                
            for i, team in enumerate(home_top):
                if i <= 4:
                    teamname , score = team
                    point_label = Label(master,text=f"{teamname} - [{score}]",justify="center",padx=5,pady=2)
                    point_label.grid(row=20+i,column=ii+1)
                else:
                    break
            
            for i, team in enumerate(away_top):
                if i <= 4:
                    teamname , score = team
                    point_label = Label(master,text=f"{teamname} - [{score}]",justify="center",padx=5,pady=2)
                    point_label.grid(row=26+i,column=ii+1)
                else:
                    break
                
        
            
                
    
    def recent_gameweeks(self,season:str)->list[int]:
        recent_gameweeks = list([x[0] for x in DB_CURSOR.execute("SELECT DISTINCT Gameweek FROM 'Results' WHERE season = ? GROUP BY Gameweek HAVING ResultAdded = 1 ORDER BY Gameweek DESC",(season,)).fetchall()])
        # recent_gameweeks = [x[0] for x in DB_CURSOR.execute("SELECT gameweek FROM Data_Commits WHERE season = 'Results' AND DataAdded = 1")][::-1]
        if len(recent_gameweeks)>5:
            return recent_gameweeks[:5]
        else:
            return recent_gameweeks