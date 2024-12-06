import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, MultiPoint, Polygon
from shapely.geometry.base import BaseGeometry
from scipy.spatial import ConvexHull

file_path = "Munnar_Zones_Final.csv"  
data = pd.read_csv(file_path)

if data[['Latitude', 'Longitude', 'Pincode']].isnull().any().any():
    print("Warning: Missing values found in Latitude, Longitude, or Pincode.")
    data = data.dropna(subset=['Latitude', 'Longitude', 'Pincode'])

data['geometry'] = data.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)

gdf = gpd.GeoDataFrame(data, geometry='geometry')

gdf.set_crs(epsg=4326, inplace=True)

def create_polygon(group):
    points = group['geometry'].apply(lambda p: (p.x, p.y)).tolist()
    try:
        if len(points) > 2:
            hull = ConvexHull(points)
            polygon = Polygon([points[i] for i in hull.vertices])
        else:
            polygon = MultiPoint(points).convex_hull 
    except Exception as e:
        print(f"Error creating polygon for points: {points}, error: {e}")
        polygon = None
    return polygon

polygon_dict = gdf.groupby('Pincode').apply(create_polygon)

polygon_dict = polygon_dict.dropna()

polygon_gdf = gpd.GeoDataFrame(polygon_dict, columns=['geometry'], crs='EPSG:4326')

polygon_gdf['Pincode'] = polygon_gdf.index

polygon_gdf.reset_index(drop=True, inplace=True)

polygon_gdf['geometry'] = polygon_gdf['geometry'].apply(
    lambda geom: geom if geom.is_valid and geom.geom_type == 'Polygon' else geom.buffer(0.001)
)

final_gdf = polygon_gdf.merge(
    gdf.drop_duplicates(subset=['Pincode']),
    on='Pincode',
    how='left'
).drop(columns=['geometry_y']).rename(columns={'geometry_x': 'geometry'})

final_gdf.to_file("Munnar_pincode_zones.geojson", driver="GeoJSON") 
final_gdf.to_file("Munnar_pincode_zones.shp")

final_gdf['geometry'] = final_gdf['geometry'].apply(lambda geom: geom.wkt)
final_gdf.to_csv("Munnar_pincode_zones.csv", index=False)

print("Polygon creation and dataset export completed successfully!")
