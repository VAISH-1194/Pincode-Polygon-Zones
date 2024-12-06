import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

file_path = 'Munnar_Zones_Final.xlsx'

try:
    data = pd.read_excel(file_path) 
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

geolocator = Nominatim(user_agent="your_unique_email@example.com")  

def get_pincode(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        if location and 'address' in location.raw:
            return location.raw['address'].get('postcode', 'Pincode Not Found')
    except GeocoderTimedOut:
        return 'Geocoder Timeout'
    except GeocoderServiceError as e:
        return f"Service Error: {e}"
    except Exception as e:
        return f"Error: {e}"

if 'Pincode' in data.columns and 'Latitude' in data.columns and 'Longitude' in data.columns:
    for index, row in data.iterrows():
        if row['Pincode'] == "Unknown":
            fetched_pincode = get_pincode(row['Latitude'], row['Longitude'])
            data.at[index, 'Pincode'] = fetched_pincode
            print(f"Pincode of row {index + 1} - {fetched_pincode}")
            time.sleep(1)
        else:
            print(f"Pincode of row {index + 1} - {row['Pincode']} (already exists)")
else:
    print("The dataset does not contain required columns: 'Latitude', 'Longitude', 'Pincode'")
    exit()

output_file = 'output_with_pincodes_munnar.xlsx'
try:
    data.to_excel(output_file, index=False) 
    print(f"Pincode fetching completed. Updated file saved as {output_file}.")
except Exception as e:
    print(f"Error saving file: {e}")


















