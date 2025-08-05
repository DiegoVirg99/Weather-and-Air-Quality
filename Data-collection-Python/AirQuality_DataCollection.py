import pandas as pd
import time
from datetime import datetime
from sqlalchemy import create_engine
import urllib
from get_coordinates import get_coordinates
from get_quality_data import get_air_quality_data


cities = ["New Delhi", "New York", "Tokyo", "Bejing", "Sydney", "Berlin", "Madrid", "London", "Paris", "Rome"]


start = "2025-07-08"
end = "2025-07-28"

air_quality_data = []
for city in cities:

    coord = get_coordinates(city)
    city_air_quality = get_air_quality_data(coord[0], coord[1], start, end, city)
    air_quality_data.append(city_air_quality)
    time.sleep(1)
    print(f"Collected data for {city}")

# Concatenate all city data into a single DataFrame
air_quality_data = pd.concat(air_quality_data, ignore_index=True).drop(columns=['no'])

print(air_quality_data)

# SQL Server connection
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=AirQualityDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# Save DataFrame to SQL Server
air_quality_data.to_sql(name='AirQuality_Data', con=engine, if_exists='append', index=False)