from shapely.geometry import Point, Polygon
import pandas as pd
import geopandas as gpd
from geopy.distance import geodesic
import re

pd.set_option('display.max_columns', None)

pavingschedule_df = gpd.read_file('pavingscheduleimg.geojson')

length_of_road_col = []
for i in pavingschedule_df['geometry']:
    coordinates_string = re.search('LINESTRING \((.*)\)', str(i))
    coordinates_list = coordinates_string.group(1).split(',')
    coordinates_geometric = []
    for l in coordinates_list:
        lat = l.strip().split(" ")[1]
        lng = l.strip().split(" ")[0]
        coordinates_geometric.append(eval("(" + lat + ", " + lng + ")"))

    length_of_road = 0.0
    for i in range(len(coordinates_geometric) - 1):
        length_of_road += geodesic(coordinates_geometric[i], coordinates_geometric[i+1]).meters

    print(length_of_road)

    length_of_road_col.append(length_of_road)

    print(len(coordinates_geometric))
    print(coordinates_geometric)
    print(type(coordinates_geometric[0]))

print(length_of_road_col)

pavingschedule_df['Length of Paved Road (meters)'] = length_of_road_col

# Convert geojson file into excel
pavingschedule_df.to_excel("pavingschedulegeojson.xlsx")


