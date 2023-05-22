from dataclasses import dataclass
import sqlite3

DB_CONNECTION = sqlite3.connect('Prediction_Game.db')
DB_CURSOR = DB_CONNECTION.cursor()

@dataclass
class PlayerPrediction():
    player      :str
    home_team   :str
    home_score  :int
    away_team   :str
    away_score  :str

