import requests # type: ignore

def get_coordinates(city_name):

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city_name,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'MyGetCoordinates (diegovirgili99@gmail.com)'  
    }

    response = requests.get(url, params=params, headers=headers)

    data = response.json()

    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return float(lat), float(lon)
    else:
        return None, None
    

    