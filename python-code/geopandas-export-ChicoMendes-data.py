#! /home/mzamith/Apps/anaconda3/bin/python
import os
import sys
import math
import pandas as pd
import geopandas
from geopandas import GeoSeries
from shapely.geometry import Polygon, MultiPolygon
import numpy as np
import matplotlib.pyplot as plt
from shapely import wkt
#from pyproj import Proj, transform
from pyproj import Transformer
import ufrrjgeo
if __name__ == "__main__":
    print('Load Lagos e Lagoas')
    enco           = 'ISO-8859-1'
    discretization = 50
    lakes     = geopandas.read_file('/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/Lagos-Lagoa/amb_app_lagoas_25k_inea.shp', encodig=enco)
    region    = geopandas.read_file('/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/Unidade-Conservacao/amb_ucs.shp', encodig=enco)
    mesh      = geopandas.read_file('/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-rb/recreio-dos-bandeirantes-050.shp', encodig='utf-8')
    my_lake   = lakes.loc[lakes['id'] ==  957]
    my_region = region.loc[region['id'] ==  897]

    x_g_max, x_g_min, y_g_max, y_g_min = ufrrjgeo.extrac_bounding_box(mesh)
    x_delta, y_delta = ufrrjgeo.convert_meters2latlong(discretization, discretization)

    print('Global bounding box:', x_g_max, ' ', x_g_min, ' ', y_g_max, ' ', y_g_min)
    print('     Discrete delta:', x_delta, ' ', y_delta, ' -> ', discretization, ' (m)')

    mesh['states'] = 1 #occupied
    mesh = ufrrjgeo.addAttribSetValueFromPoly(mesh, 'states', my_region, 0, x_g_min - (10*x_delta))
    mesh = ufrrjgeo.addAttribSetValueFromPoly(mesh, 'states', my_lake, 2, x_g_min - (10*x_delta))
    mesh.to_file('/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-rb/chico-mendes-malha-050.shp')
    my_lake.to_file('/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-rb/chico-mendes-lago.shp')
    my_region.to_file('/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-rb/chico-mendes-parque.shp')
