import pandas as pd
from db_link import DB_CONNECTION

data = pd.read_sql_query("SELECT * FROM 'Results'",DB_CONNECTION)
DB_CONNECTION.close()
data = data.dropna()

data.to_csv("ResultData.csv")
