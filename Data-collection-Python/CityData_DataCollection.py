import pandas as pd
import time
from get_info_city_pop import get_city_info # type: ignore
from sqlalchemy import create_engine
import urllib

# cities = ["London", "Paris", "Rome", "Berlin", "Madrid"]
cities = ["New Delhi", "New York", "Tokyo", "Bejing", "Sydney"]

city_data = []
for city in cities:
    info = get_city_info(city)
    city_data.append(info)
    time.sleep(1)  # Respect GeoNames API limits

df = pd.DataFrame(city_data)

print(df)

# SQL Server connection
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=CityDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# Save DataFrame to SQL Server
df.to_sql(name='City_Data', con=engine, if_exists='append', index=False)