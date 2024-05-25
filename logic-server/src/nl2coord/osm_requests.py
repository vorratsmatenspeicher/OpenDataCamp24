import requests
import time

# Funktion zur Durchführung einer API-Anfrage mit einem 1-Sekunden-Delay
def query_nominatim(params):
    url = "https://nominatim.openstreetmap.org/search"
    response = requests.get(url, params=params)
    time.sleep(1)  # 1-Sekunden-Delay
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_bounding_boxes(params):
    results = query_nominatim(params)
    bounding_boxes = []

    if results:
        for result in results:
            if 'boundingbox' in result:
                bounding_boxes.append(result['boundingbox'])
    else:
        print(f"Cannot find location for {params['q']}")
    
    return bounding_boxes

# Beispiel zur Nutzung der Funktion
# if __name__ == "__main__":
#     # Erster Parameter der Anfrage
#     params1 = {
#         'format': 'json',
#         'q': 'Hochschulstraße Dresden Saxony Germany'
#     }

#     # Zweiter Parameter der Anfrage
#     params2 = {
#         'format': 'json',
#         'q': 'Brühlsche Terrasse Dresden Saxony Germany'
#     }

#     # Durchführung der Anfragen und Abruf der Bounding-Boxen
#     array1 = get_bounding_boxes(params1)
#     array2 = get_bounding_boxes(params2)

#     # Speichern der Bounding-Boxen in einer Datei für die spätere Nutzung
#     import json
#     with open('bounding_boxes.json', 'w') as f:
#         json.dump({'array1': array1, 'array2': array2}, f)
    
#     print(f"Bounding boxes for params1: {array1}")
#     print(f"Bounding boxes for params2: {array2}")
