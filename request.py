import request

url=r"https://kommisdd.dresden.de/net4/public/ogcapi/collections/L1625/items?filter=messzeit>“2024-05-01 06:00:00” and messzeit<“2024-05-02 06:00:00" and ids==920 and parameter~~“Lufttemperatur”&propertynames=geom,ids,messzeit,wert_n,einheit,bezeichnung,parameter"

"""

x = requests.get(url)

print(x)

