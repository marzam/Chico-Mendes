#! /home/mzamith/Apps/anaconda3/bin/python
import os
import sys
import math
import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries
from shapely.geometry import Polygon, MultiPolygon
import numpy as np
import matplotlib.pyplot as plt
from shapely import wkt
#from pyproj import Proj, transform
from pyproj import Transformer
'''
df = pd.DataFrame(
    {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
     'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
     'Coordinates': ['POINT(-58.66 -34.58)', 'POINT(-47.91 -15.78)',
                     'POINT(-70.66 -33.45)', 'POINT(-74.08 4.60)',
                     'POINT(-66.86 10.48)']})
df['Coordinates'] = gpd.GeoSeries.from_wkt(df['Coordinates'])
gdf = gpd.GeoDataFrame(df, geometry='Coordinates')
print(gdf.head())
'''

x_max = -43.09690430442349
x_min = -43.7954747904931
y_max = -22.746032828628106
y_min = -23.082905638411873
delta_x = 0.00044915764205976066
delta_y = 0.0004491576420551603
#delta_x = 0.5
#delta_y = 0.5
x = x_min
y = y_min
ID = 0
ID_v     = []
COORD_v  = []
#we must to close polygon, it means, the last point must be equal to the first one
while y <= y_max:
    x = x_min#
    while x <= x_max:
        s_poly = 'POLYGON (({0:.20f} {1:.20f}, {2:.20f} {1:.20f}, {2:.20f} {3:.20f}, {0:.20f} {3:.20f}, {0:.20f} {1:.20f}))'.format(x, y, x + delta_x, y + delta_y)
        ID_v.append(ID)
        COORD_v.append(s_poly)
        x = x + delta_x
        ID = ID + 1
        if ID % 100:
            print('Running...')
    y = y + delta_y

print('Creating dataframe')
df=pd.DataFrame({'id':ID_v, 'geometry':COORD_v})

print('Creating geoseries')
df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
gdf = gpd.GeoDataFrame(df, geometry='geometry')
x, y = gdf.iloc[0].geometry.centroid.xy
print(x[0])
print(y[0])
#print('Saving file')
#gdf.to_file("mesh.shp")
#print('Creating numpy...')
#my_array = np.array([[ID_v], [COORD_v]])
#print('Creating dataframe...')
#df = pd.DataFrame(my_array, columns = ['id','geometry'])
#print(df.iloc[1])
#df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
#print('Coordinate created')
#input('Continue ???')

#df['Coordinates'] = gpd.GeoSeries.from_wkt(df['Coordinates'])
#gdf = gpd.GeoDataFrame(df, geometry='Coordinates')
#print(df.head())
