from sqlalchemy import create_engine
import urllib
import pandas as pd

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=MeteoDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

query = "SELECT * FROM Meteo_daily WHERE city = 'Paris' AND tavg > 20"
df = pd.read_sql(query, engine)
print(df)