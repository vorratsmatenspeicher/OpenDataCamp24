import json
import hashlib
import os
from .osm_requests import get_bounding_boxes, query_nominatim
from .coord_intersection import find_first_intersection
from .nl_interpreter import convert_location

CACHE_DIR = 'cache'

# Erstelle das Cache-Verzeichnis, wenn es nicht existiert
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def generate_cache_key(params):
    # Erstellen eines eindeutigen Hashes basierend auf den Anfrageparametern
    hash_input = json.dumps(params, sort_keys=True).encode('utf-8')
    return hashlib.md5(hash_input).hexdigest()

def load_from_cache(cache_key):
    cache_path = os.path.join(CACHE_DIR, cache_key)
    if os.path.exists(cache_path):
        with open(cache_path, 'r') as cache_file:
            return json.load(cache_file)
    return None

def save_to_cache(cache_key, data):
    cache_path = os.path.join(CACHE_DIR, cache_key)
    with open(cache_path, 'w') as cache_file:
        json.dump(data, cache_file)

def get_bounding_boxes_with_cache(params):
    cache_key = generate_cache_key(params)
    cached_data = load_from_cache(cache_key)
    if cached_data is not None:
        print("using cached data for params")
        return cached_data
    
    data = get_bounding_boxes(params)
    save_to_cache(cache_key, data)
    return data

def get_coords(text):
    instructions_json = convert_location(text).strip()

    print(f"{instructions_json!r}")
    # Parse the JSON response
    instructions = json.loads(instructions_json)
    
    print(instructions)
    function_name = instructions['function']
    parameters = instructions['parameters']

    # Rufe die entsprechende Funktion mit den Parametern auf
    if function_name in function_mapping:
        function_to_call = function_mapping[function_name]
        function_result = function_to_call(*parameters)
        print(function_result)
        return function_result
    else:
        print(f"Unbekannte Funktion: {function_name}")
    
    return None

def add_general_location(query):
    return query+" Dresden Saxony Germany"

# Beispiel-Funktionen, die aufgerufen werden sollen
def intersection(query_a, query_b):
    query_a = add_general_location(query_a)
    query_b = add_general_location(query_b)
    print(query_a, query_b)
    # Laden der Bounding-Boxen mit Cache
    array1 = get_bounding_boxes_with_cache(query_a)
    array2 = get_bounding_boxes_with_cache(query_b)

    print(array1)
    print(array2)
    # Finde den ersten Schnittpunkt
    coords = find_first_intersection(array1, array2)
    return coords

def distance(a: tuple, b: tuple) -> float:
    return (((a[0] * b[0])**2 + (a[1] * b[1])**2)**0.5)


def distance(a: tuple, b: tuple) -> float:
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def closestPoint(query_a, query_b):
    print(f"Aufruf von closestPoint mit {query_a} und {query_b}")
    query_a = add_general_location(query_a)
    query_b = add_general_location(query_b)
    results_a = query_nominatim(query_a)
    results_b = query_nominatim(query_b)
    
    if not results_a or not results_b:
        print(f"Cannot find location for {query_a} or {query_b}")
        return (0, 0)
    
    smaller = results_a if len(results_a) <= len(results_b) else results_b
    bigger = results_a if len(results_a) > len(results_b) else results_b
    
    pos_1 = ()
    if smaller:
        first = smaller[0]
        if 'lat' in first and 'lon' in first:
            pos_1 = (float(first['lat']), float(first['lon']))
    
    if not pos_1:
        print(f"Cannot find a valid location in {smaller}")
        return (0, 0)

    nearest = { 
        "distance": float('inf'),
        "position": (0, 0)
    }

    for e in bigger:
        if 'lat' in e and 'lon' in e:
            pos = (float(e['lat']), float(e['lon']))
            ad = distance(pos_1, pos)
            if ad < nearest["distance"]:
                nearest["distance"] = ad
                nearest["position"] = (float(e['lat']), float(e['lon']))

    if nearest["distance"] == float('inf'):
        print(f"Cannot find a closer location for {query_a} and {query_b}")
        return (0, 0)

    return nearest["position"]

def getCoords(query):
    query = add_general_location(query)
    results = query_nominatim(query)
    if results:
        first = results[0]
        if 'lat' in first and 'lon' in first:
            return float(first['lat']), float(first['lon'])
    else:
        print(f"Cannot find location for {query}")
    return None

# Mapping der Funktionsnamen zu den tatsächlichen Funktionen
function_mapping = {
    "intersection": intersection,
    "closestPoint": closestPoint,
    "getCoords": getCoords
}

# Beispiel zur Nutzung der Funktion
if __name__ == "__main__":
    coords = get_coords("Markthalle in der Nähe vom Goldenen Reiter")

    # Ausgabe der Ergebnisse
    if coords:
        print(f"Coords: {coords}")
    else:
        print("Keine Coords")
