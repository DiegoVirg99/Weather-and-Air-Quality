from meteostat import Hourly, Point
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import urllib
from get_coordinates import get_coordinates # type: ignore


# List of cities to collect data for
# cities = ["London", "Paris", "Rome", "Berlin", "Madrid"]
cities = ["New Delhi", "New York", "Tokyo", "Bejing", "Sydney", "London", "Paris", "Rome", "Berlin", "Madrid"]

start = datetime(2025, 7, 9, 23, 59)
end = datetime(2025, 7, 28, 23, 59)

all_data = []

for city in cities:
    lat, lon = get_coordinates(city)
    location = Point(lat, lon)
    df = Hourly(location, start, end).fetch()
    df.reset_index(inplace=True)
    df['city'] = city
    all_data.append(df)

# Combine all city data into a single DataFrame
df_all = pd.concat(all_data, ignore_index=True)
print(df_all.head())
print(df_all.tail())

# SQL Server connection
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=MeteoDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# Save DataFrame to SQL Server
df_all.to_sql(name='Meteo_Hourly', con=engine, if_exists='append', index=False)