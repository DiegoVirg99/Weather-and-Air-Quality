from meteostat import Daily, Point
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import urllib
import time
from get_coordinates import get_coordinates  # type: ignore


# List of cities to collect data for
# cities = ["London", "Paris", "Rome", "Berlin", "Madrid"]
cities = ["New Delhi", "New York", "Tokyo", "Bejing", "Sydney", "London", "Paris", "Rome", "Berlin", "Madrid"]

start = datetime(2020, 1, 1)
end = datetime(2025, 7, 28)

all_data = []

for city in cities:
    lat, lon = get_coordinates(city)
    location = Point(lat, lon)
    df = Daily(location, start, end).fetch()
    df.reset_index(inplace=True)
    df['city'] = city
    df['latitude'] = lat
    df['longitude'] = lon
    all_data.append(df)
    time.sleep(1)  # Sleep to avoid hitting API rate limits

# Combine all city data into a single DataFrame
df_all = pd.concat(all_data, ignore_index=True)
print(df_all.head())

# SQL Server connection
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=MeteoDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# Save DataFrame to SQL Server
df_all.to_sql(name='Meteo_Daily', con=engine, if_exists='append', index=False)
