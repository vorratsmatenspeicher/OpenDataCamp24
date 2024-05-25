# request weather data from klips
# Zeit + Ort -> Wetter

import requests
import json
import datetime
from urllib import parse

latLonMargins=0.02

def get_nearest_id(coord: tuple[float, float]) -> int:
    def dist_to(id: int) -> float:
        lat, lon = coord
        lat_closest, lon_closest = IDS[id]

        dist = (lat - lat_closest) ** 2 + (lon - lon_closest) ** 2

        if dist[0] > latLonMargins or dist[1] > latLonMargins:
            raise ValueError("Closest data point is far away.")

        return dist
        
    return min(IDS, key=dist_to)

def get_weather(ids: int, date: str):
    try:
        date = datetime.datetime.strptime(date, date_fmt)
    except Exception:
        print("WARNING: trouble converting string to date")
    try:
        t_1 = datetime.datetime.strftime(date - datetime.timedelta(hours=2), date_fmt)
        t_2 = datetime.datetime.strftime(date + datetime.timedelta(hours=2), date_fmt)
    except Exception:
        print("WARNING: trouble converting date to string")

    base_url = 'https://kommisdd.dresden.de/net4/public/ogcapi/collections/L1625/items'
    time_filter = f'?filter=messzeit>"{t_1}" and messzeit<"{t_2}"'
    ids_filter = f' and ids=={ids}'
    temp_filter = 'and parameter~~"Lufttemperatur"&propertynames=ids,parameter,wert_n,messzeit'

    temp_url = base_url + time_filter + ids_filter + temp_filter

    print(f"temp_url: {temp_url}")

    try:
        req = requests.get(temp_url)  # request data
    except Exception:
        print(f"WARNING: trouble requesting data from {temp_url}")
    try:
        req_json = json.loads(req.text)  # parse json
    except Exception:
        print("WARNING: trouble converting requested text to JSON")

    return req_json


def request(coord: tuple[float, float], str_date: str):
    try:
        nearest_id = get_nearest_id(coord)
    except Exception:
        print("WARNING: trouble in nearest_id()")

    print(f"nearestID: {nearest_id}")

    try:
        weather_json = get_weather(nearest_id, str_date)
    except Exception:
        print("WARNING: trouble in get_weather()")

    try:
        weather_list = [(entry['properties']['messzeit'], entry['properties']['wert_n']) for entry in weather_json['features']]
    except Exception:
        print("WARNING: trouble writing JSON to list")
    return weather_list


date_fmt = "%Y-%m-%d %H:%M:%S"
str_date = "2024-05-01 06:00:00"
coord = [13.7312841000004, 51.0442978999856]

try:
    date = datetime.datetime.strptime(date, date_fmt)
except Exception:
    print("WARNING: trouble converting string to date")
try:
    t_1 = datetime.datetime.strftime(date - datetime.timedelta(hours=2), date_fmt)
    t_2 = datetime.datetime.strftime(date + datetime.timedelta(hours=2), date_fmt)
except Exception:
    print("WARNING: trouble converting date to string")

id_url = f'https://kommisdd.dresden.de/net4/public/ogcapi/collections/L1625/items?filter=messzeit>"{t_1}" and messzeit<"{t_2}"&propertynames=geom,ids'

try:
    req = requests.get(id_url)  # request data
except Exception:
    print(f"WARNING: trouble requesting data from {id_url}")

try:
    req_json = json.loads(req.text)  # parse json
except Exception:
    print("WARNING: trouble converting requested text to JSON")

IDS = {}

for feature in req_json['features']:
    if feature['id'] in IDS:
        continue

    try:
        IDS[feature['id']] = feature['geometry']['coordinates']
    except Exception:
        print("WARNING: trouble retrieving id")

print(f"number of distinct ids: {len(IDS)}")
