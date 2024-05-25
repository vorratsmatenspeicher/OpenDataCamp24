import json
import hashlib
import os
from osm_requests import get_bounding_boxes
from coord_intersection import find_first_intersection

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
        return cached_data
    
    data = get_bounding_boxes(params)
    save_to_cache(cache_key, data)
    return data

def get_coords(text):
    # Erster Parameter der Anfrage
    params1 = {
        'format': 'json',
        'q': 'Eisenstuckstraße Dresden Saxony Germany'
    }

    # Zweiter Parameter der Anfrage
    params2 = {
        'format': 'json',
        'q': 'Liebigstraße Dresden Saxony Germany'
    }

    # Laden der Bounding-Boxen mit Cache
    array1 = get_bounding_boxes_with_cache(params1)
    array2 = get_bounding_boxes_with_cache(params2)

    # Finde den ersten Schnittpunkt
    coords = find_first_intersection(array1, array2)
    return coords

# Beispiel zur Nutzung der Funktion
if __name__ == "__main__":
    coords = get_coords("Hochschulstraße Ecke Schnorrstraße Dresden Saxony Germany")

    # Ausgabe der Ergebnisse
    if coords:
        print(f"Coords: {coords}")
    else:
        print("Keine Coords")
