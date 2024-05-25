def calculate_intersection(box1, box2):
    min_lat1, max_lat1, min_lon1, max_lon1 = map(float, box1)
    min_lat2, max_lat2, min_lon2, max_lon2 = map(float, box2)

    intersect_min_lat = max(min_lat1, min_lat2)
    intersect_max_lat = min(max_lat1, max_lat2)
    intersect_min_lon = max(min_lon1, min_lon2)
    intersect_max_lon = min(max_lon1, max_lon2)

    if intersect_min_lat < intersect_max_lat and intersect_min_lon < intersect_max_lon:
        return (intersect_min_lat, intersect_max_lat, intersect_min_lon, intersect_max_lon)
    else:
        return None

def find_first_intersection(array1, array2):
    for box1 in array1:
        for box2 in array2:
            intersection = calculate_intersection(box1, box2)
            if intersection:
                center = calculate_center(intersection)
                if center:
                    return center
    return None

def calculate_center(intersection):
    if intersection:
        min_lat, max_lat, min_lon, max_lon = intersection
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        return (center_lat, center_lon)
    return None

# Beispiel zur Nutzung der Funktionen
# if __name__ == "__main__":
#     # Beispiel-Arrays von Bounding-Boxen
#     array1 = [
#         ["51.0338047", "51.0342438", "13.7404485", "13.7426374"],
#         ["30.0", "35.0", "20.0", "25.0"]
#     ]
#     array2 = [
#         ["52.0", "58.0", "12.0", "18.0"],
#         ["40.0", "45.0", "22.0", "28.0"]
#     ]

#     # Finde den ersten Schnittpunkt
#     first_intersection = find_first_intersection(array1, array2)

#     # Ausgabe der Ergebnisse
#     if first_intersection:
#         print(f"Erster Schnittpunkt: {first_intersection}")
#     else:
#         print("Kein Schnittpunkt vorhanden")
