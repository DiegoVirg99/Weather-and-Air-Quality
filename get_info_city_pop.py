import requests

# --- Config ---
GEONAMES_USERNAME = 'diegovirg'

def get_geoname_id(city_name):
    search_url = "http://api.geonames.org/searchJSON"
    params = {
        'q': city_name,
        'maxRows': 1,
        'featureClass': 'P',
        'username': GEONAMES_USERNAME
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json().get("geonames", [])
        if results:
            return results[0]['geonameId']
    return None

def get_city_details(geoname_id):
    detail_url = "http://api.geonames.org/getJSON"
    params = {
        'geonameId': geoname_id,
        'username': GEONAMES_USERNAME
    }
    response = requests.get(detail_url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_city_info(city_name):
    geoname_id = get_geoname_id(city_name)
    if not geoname_id:
        return {'City': city_name, 'error': 'GeonameId not found'}
    
    details = get_city_details(geoname_id)
    if not details:
        return {'City': city_name, 'error': 'Details not found'}
    
    return {
        'City': details.get('name'),
        'Country': details.get('countryName'),
        'Admin1': details.get('adminName1'),
        'Admin2': details.get('adminName2'),
        'Population': details.get('population'),
        'Latitude': float(details.get('lat')),
        'Longitude': float(details.get('lng')),
        'Altitude_m': details.get('elevation'),
        'Timezone': details.get('timezone', {}).get('timeZoneId')
    }
