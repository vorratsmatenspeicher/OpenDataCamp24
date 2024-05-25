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

def calculate_center(intersection):
    if intersection:
        min_lat, max_lat, min_lon, max_lon = intersection
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        return (center_lat, center_lon)
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

# Beispiel zur Nutzung der Funktionen
if __name__ == "__main__":
    # Beispiel-Arrays von Bounding-Boxen
    array1 = [['51.3216391', '51.3217049', '12.3422793', '12.3425763'], ['51.0342438', '51.0347012', '13.7381717', '13.7404485'], ['51.0359965', '51.0361466', '13.7307093', '13.7315572'], ['48.2772171', '48.2780735', '8.8647386', '8.8682200'], ['51.0331287', '51.0338047', '13.7426374', '13.7455491'], ['48.1525027', '48.1532535', '11.5716548', '11.5742201'], ['51.5808306', '51.5820204', '7.1172588', '7.1178284'], ['49.4115354', '49.4146687', '11.1007448', '11.1023310'], ['51.0362834', '51.0363690', '13.7291329', '13.7300334']]
    array2 = [['51.0340351', '51.0370853', '13.7329689', '13.7344272'], ['51.0305421', '51.0324381', '13.7313031', '13.7322134'], ['47.8668666', '47.8668747', '12.1100912', '12.1101819'], ['49.8771194', '49.8775924', '8.6555184', '8.6568705'], ['50.9092590', '50.9093486', '8.0298071', '8.0302604'], ['50.9092402', '50.9159057', '8.0274124', '8.0313259'], ['49.8768890', '49.8769446', '8.6556643', '8.6557121'], ['51.0359629', '51.0365503', '13.7334122', '13.7336850'], ['46.9494236', '46.9496524', '7.4354027', '7.4364982']]

    # Finde den ersten Schnittpunkt
    first_intersection = find_first_intersection(array1, array2)

    # Ausgabe der Ergebnisse
    if first_intersection:
        print(f"Erster Schnittpunkt: {first_intersection}")
    else:
        print("Kein Schnittpunkt vorhanden")
