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
from pyproj import Transformer
if __name__ == "__main__":
    print('Working with geopandas')
    print('Load data')
    neighborhood = gpd.read_file('../bairros_populacao.shp', encodig='ISO-8859-1')
    RJ_city = neighborhood.loc[neighborhood['municipio'] == 'RIO DE JANEIRO']
    JG_neighborhood = RJ_city.loc[RJ_city['bairro'] == 'JARDIM GUANABARA']
    print(JG_neighborhood.geometry)
    g = [i for i in JG_neighborhood.geometry]
    x,y = g[0].exterior.coords.xy
    coords = np.dstack((x,y)).tolist()
    #print(coords)
    x_max = coords[0][0][0]
    x_min = coords[0][0][0]
    y_max = coords[0][0][1]
    y_min = coords[0][0][1]

    for i in range(1, len(coords[0])):
        x_max = max(x_max, coords[0][i][0])
        x_min = min(x_max, coords[0][i][0])
        y_max = max(y_max, coords[0][i][1])
        y_min = min(y_max, coords[0][i][1])

        #print(coords[0][i][0], ' ', coords[0][i][1])

    print('x_max: ', x_max, ' x_min: ', x_min, ' | y_max: ', y_max, ' y_min: ', y_min)
    #print(max(1, -1))
    #print(g[0].boundary)
'''
    all_coords = []
    for b in g[0].boundary: # for first feature/row
        coords = np.dstack(b.coords.xy).tolist()
        all_coords.append(*coords)

    print(all_coords)
'''
