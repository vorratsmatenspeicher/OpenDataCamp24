import json
import hashlib
import os
import dotenv
import requests
import time

CACHE_DIR = 'cache'

dotenv.load_dotenv()

# Create the cache directory if it doesn't exist
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def generate_cache_key(params):
    # Create a unique hash based on the request parameters
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


def query_nominatim(query):
    cache_key = generate_cache_key(query)
    cached_data = load_from_cache(cache_key)
    if cached_data is not None:
        print("Using cached data for params")
        return cached_data
    
    url = os.environ.get("NOMINATIM_URL") or "https://nominatim.openstreetmap.org/search"
    print("Nominatim request to {url}")
    params = {
        'format': "json",
        'q': query
    }
    response = requests.get(url, params=params)
    time.sleep(2)  # 1-second delay to respect usage policies
    if response.status_code == 200:
        print(response)
        data = response.json()
        save_to_cache(cache_key, data)  # Save the response in the cache
        return data
    elif response.status_code == 403:
        raise Exception(f"Nominatim API blocked us, too many requests. {response.status_code}")
    else:
        raise Exception(f"Nominatim API returned wrong statuscode. {response.status_code}")


def get_bounding_boxes(query):
    results = query_nominatim(query)
    bounding_boxes = []

    if results:
        for result in results:
            if 'boundingbox' in result:
                bounding_boxes.append(result['boundingbox'])
    else:
        print(f"Cannot find location for {query}")

    return bounding_boxes
