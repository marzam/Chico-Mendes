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
#from pyproj import Proj, transform
from pyproj import Transformer
import ufrrjgeo

def select_city_district(shp_file_name, enco, state_name, district_name, discretization, mesh_name):
    print('Loading shop file: ', shp_file_name)
    state = gpd.read_file(shp_file_name, encodig=enco)
    x_g_max, x_g_min, y_g_max, y_g_min = ufrrjgeo.extrac_bounding_box(state)
    print('Selecting city: ', state_name)
    city  = state.loc[state['municipio'] == state_name]

    print('Selecting district: ', district_name)

    district = city.loc[city['bairro'] == district_name]
    print('Creating bounding box')

    x_max, x_min, y_max, y_min = ufrrjgeo.extrac_bounding_box(district) #It gets bounding box from city, district or whatever that has geometry with poly and muily
    x_dist = x_max - x_min
    y_dist = y_max - y_min
    x_delta, y_delta = ufrrjgeo.convert_meters2latlong(discretization, discretization)
    #Defining the boundary - 2cells added at ending and beging
    x_max = x_max + (2 * x_delta)
    x_min = x_min - (2 * x_delta)
    y_max = y_max + (2 * y_delta)
    y_min = y_min - (2 * y_delta)

    w = int(math.ceil(x_dist / x_delta))
    h = int(math.ceil(y_dist / y_delta))

    print('      Bounding box:', x_max, ' ', x_min, ' ', y_max, ' ', y_min)
    print('Global bounding box:', x_g_max, ' ', x_g_min, ' ', y_g_max, ' ', y_g_min)
    print('     Discrete delta:', x_delta, ' ', y_delta, ' -> ', discretization, ' (m)')
    print('               dist:', x_dist, ' ', y_dist)
    print('     Width / height:', w, h)

    #informar a quantidade de atributos
    mesh = ufrrjgeo.create_geoseries(city, x_delta, y_delta, x_max, x_min, y_max,  y_min)
    mesh = ufrrjgeo.build_mesh_geometry(mesh, district, x_g_min - (10*x_delta), district_name)

    print('Getting neighborhood info....')
    for i in range(0, len(city)):
        district = city.loc[city['bairro'] == city.iloc[i].bairro]
        mesh = ufrrjgeo.build_mesh_geometry(mesh, district, x_g_min - (10*x_delta), city.iloc[i].bairro)


    mesh.to_file(mesh_name)
    #for i in range(0, len(mesh)):
    #    print()

    #mesh.iloc[0]['boundary'] = '1'
    #mesh.loc[mesh.id == 0, 'boundary'] = 1  #<--- how to update
    #print(mesh.iloc[0]['boundary'])
    #print(mesh.iloc[0]['id'])
    #show_mapa_from_geodf(district, mesh)

if __name__ == "__main__":
    print('City simulation')
    print('Use RJ city SHP file')

    shp_file_name = sys.argv[1]
    enco = 'ISO-8859-1'
    state_name = sys.argv[2]
    district_name  = sys.argv[3]
    #district_name  = 'JARDIM GUANABARA'
    discretization = int(sys.argv[5]) #in meters0
    mesh_name = sys.argv[4]

    select_city_district(shp_file_name, enco, state_name, district_name, discretization, mesh_name)



    #for i in range(0, len(mesh)):
    #    cell = mesh.iloc[i]
    #    print(cell.geometry, ' ', cell.geometry.centroid)
    #
    #for i in range(0, len(city)):
    #    extrac_bounding_box(city.iloc[i].geometry)
#Solved: https://stackoverflow.com/questions/64099107/convert-multipolygon-geometry-into-list
#Attention: It will create a list of lists
