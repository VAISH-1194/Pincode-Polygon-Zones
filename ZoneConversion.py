import json
import pandas as pd

with open("Munnar.geojson", "r", encoding="utf-8", errors="replace") as f:
    data = json.load(f)

zone_id_map = {}
zone_counter = 100

rows = []
for feature in data.get("features", []): 
    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})

    zone_name = properties.get("name", "Unnamed Zone")
    speed_limit = properties.get("maxspeed", "Unknown")
    zone_type = properties.get("highway", properties.get("amenity", properties.get("hazard", "Unknown Zone Type")))
    coordinates = geometry.get("coordinates", [])

    if isinstance(coordinates[0], list) and len(coordinates) > 1:
        lat1, lon1 = coordinates[0][1], coordinates[0][0]
        lat2, lon2 = coordinates[1][1], coordinates[1][0]
        latitude = (lat1 + lat2) / 2
        longitude = (lon1 + lon2) / 2
    elif len(coordinates) == 2:
        longitude, latitude = coordinates
    else:
        latitude = "Unknown"
        longitude = "Unknown"

    if zone_name == "Unnamed Zone":
        zone_id = "-"  
    else:
        if zone_name not in zone_id_map:
            zone_id = f"Z{zone_counter}"
            zone_id_map[zone_name] = zone_id
            zone_counter += 1
        else:
            zone_id = zone_id_map[zone_name]

    rows.append(["Munnar", zone_id, zone_name, zone_type, speed_limit, latitude, longitude, "Unknown"])

df = pd.DataFrame(rows, columns=["District", "Zone ID", "Zone Name", "Zone Type", "Zone Speed Limit", "Latitude", "Longitude", "Pincode"])
df.to_excel("Munnar_Zones_Final.xlsx", index=False)
print("Excel file saved!")