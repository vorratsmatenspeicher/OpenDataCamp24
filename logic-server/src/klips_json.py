# request weather data from klips
# Zeit + Ort -> Wetter
import requests
import json
import datetime
from urllib import parse

distMargin=0.03

def get_nearest_id(coord: tuple[float, float]) -> int:
    def dist_to(id: int) -> float:
        lat, lon = coord
        lat_closest, lon_closest = IDS[id]

        dist = ((lat - lat_closest) ** 2 + (lon - lon_closest) ** 2)**0.5

        # if dist > distMargin:
        #     raise Exception("No accurate data available: closest sensor is far away.")

        return dist

    return min(IDS, key=dist_to)


def get_weather(ids: int, date: str):
    date = datetime.datetime.fromisoformat(date)

    t_1 = datetime.datetime.strftime(date - datetime.timedelta(hours=2), date_fmt)
    t_2 = datetime.datetime.strftime(date + datetime.timedelta(hours=2), date_fmt)

    base_url = 'https://kommisdd.dresden.de/net4/public/ogcapi/collections/L1625/items'
    time_filter = f'?filter=messzeit>"{t_1}" and messzeit<"{t_2}"'
    ids_filter = f' and ids=={ids}'
    temp_filter = 'and parameter~~"Lufttemperatur"&propertynames=ids,parameter,wert_n,messzeit'

    temp_url = base_url + time_filter + ids_filter + temp_filter

    print(f"temp_url: {temp_url}")

    req = requests.get(temp_url)  # request data
    req_json = json.loads(req.text)  # parse json

    return req_json


def request(coord: tuple[float, float], str_date: str):
    nearest_id = get_nearest_id(coord)

    print(f"nearestID: {nearest_id}")

    try:
        weather_json = get_weather(nearest_id, str_date)
    except Exception as e:
        e.add_note("WARNING: trouble in get_weather()")
        raise

    try:
        weather_list = [(
            datetime.datetime.strptime(entry['properties']['messzeit'], "%d.%m.%Y %H:%M:%S"),
            entry['properties']['wert_n']
        ) for entry in weather_json['features']]
    except Exception as e:
        e.add_note("WARNING: trouble retrieving data from JSON")
        raise
    return weather_list


date_fmt = "%Y-%m-%d %H:%M:%S"
str_date = "2024-05-01 06:00:00"
coord = [13.7312841000004, 51.0442978999856]

try:
    date = datetime.datetime.strptime(str_date, date_fmt)
except Exception as e:
    raise Exception("WARNING: trouble converting string to date") from e
try:
    t_1 = datetime.datetime.strftime(date - datetime.timedelta(hours=2), date_fmt)
    t_2 = datetime.datetime.strftime(date + datetime.timedelta(hours=2), date_fmt)
except Exception as e:
    raise Exception("WARNING: trouble converting date to string") from e

id_url = f'https://kommisdd.dresden.de/net4/public/ogcapi/collections/L1625/items?filter=messzeit>"{t_1}" and messzeit<"{t_2}"&propertynames=geom,ids'

try:
    req = requests.get(id_url)  # request data
except Exception as e:
    raise Exception(f"WARNING: trouble requesting data from {id_url}") from e

try:
    req_json = json.loads(req.text)  # parse json
except Exception as e:
    raise Exception("WARNING: trouble converting requested text to JSON") from e

IDS = {}

for feature in req_json['features']:
    if feature['id'] in IDS:
        continue

    try:
        IDS[feature['id']] = feature['geometry']['coordinates']
    except Exception as e:
        raise Exception("WARNING: trouble retrieving id") from e

print(f"number of distinct ids: {len(IDS)}")
