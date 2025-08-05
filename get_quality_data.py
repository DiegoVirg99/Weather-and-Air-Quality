import requests
import time
import pandas as pd

API_KEY = 'faecdf6b1c1403c0aa52ced66dfa5bed'

def get_air_quality_data(lat, lon, start_date, end_date, city_name, api_key=API_KEY):
    start_time = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
    end_time = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))
    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution/history?"
        f"lat={lat}&lon={lon}&start={start_time}&end={end_time}&appid={api_key}"
    )
    response = requests.get(url)
    data = response.json()
    results = []
    for entry in data.get('list', []):
        timestamp = entry['dt']
        aqi = entry['main']['aqi']
        components = entry['components']
        result = {
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp)),
            "city": city_name,
            "aqi": aqi,
            **components
        }
        results.append(result)
        df = pd.DataFrame(results)
    return df

