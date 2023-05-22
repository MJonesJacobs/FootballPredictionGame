from web_scrape import gameweek_fixtures
import db_link
from predication_emails import send_emails

def player_list():
    player_list = db_link.DB_CURSOR.execute("SELECT * FROM 'Player List'").fetchall()
    return player_list

send_emails(player_list(),38,gameweek_fixtures(38))
