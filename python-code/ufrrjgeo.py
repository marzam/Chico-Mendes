#! /home/mzamith/Apps/anaconda3/bin/python
from __future__ import print_function
from geopandas import GeoSeries
from shapely.geometry import Polygon, MultiPolygon
from pyproj import Transformer


import os
import sys
import math
import pandas as pd
import geopandas #as gpd
import numpy as np
import matplotlib.pyplot as plt
#from pyproj import Proj, transform
import pymp
#-------------------------------------------------------------------------------
'''
Check if the mesh centroid is in or out from another geometry
In this case, geometry is always polygon or multipolygon
'''
def checkIntersect(geom, mesh, x_min, attrib_field, region_value):
    g_x, g_y = geom.exterior.coords.xy

    #coords = np.dstack((x,y)).tolist() #Getting coordiantes from polygons

    for j in range(0, len(mesh)):
        x, y = mesh.iloc[j].geometry.centroid.xy
        x_mesh = x[0]
        y_mesh = y[0]

        #x_mesh, y_mesh = mesh.iloc[0].centroid.xy
        count = 0
        for i in range(0, len(g_x)-1):
            x_p1 = g_x[i]
            y_p1 = g_y[i]
            x_p2 = g_x[i+1]
            y_p2 = g_y[i+1]

            if abs(x_p1 - x_p2) > 1E-20 and abs(y_p1 - y_p2) > 1E-20:
                x_p3 = x_mesh
                y_p3 = y_mesh

                ret = point_in_poly_faster(x_p1, y_p1, x_p2, y_p2, x_min, x_p3, y_p3)
                if ret == True:
                    count = count + 1
        #st = '{:.20f} \t {:.20f}\n'.format(x_mesh, y_mesh)

        if (count > 0) and ((count % 2) != 0):
            mesh.loc[mesh.id == j, attrib_field] = region_value

        #if (count == 0):# oout
        #    stderr_fileno.write(st)
        #elif (count % 2) == 0:# out
        #    stderr_fileno.write(st)
        #else:# in
        #    mesh.loc[mesh.id == j, 'district'] = district_name
            #stdout_fileno.write(st)
    return mesh
#-------------------------------------------------------------------------------
'''
This procedure builds a lattice based on selecting region. Basically, the cells
and their relation with space, using global postition system
We consider in this procedure a fix field name called district which is used
in our experiments
'''
def build_mesh_geometry(mesh, region, x_min, district_name):
    g = [i for i in region.geometry]

    mpoly = MultiPolygon()
    poly  = Polygon()

    if type(g[0]) == type(poly):
        print('Polygon', district_name)
        #mesh = checkIntersect(g[0], mesh, x_min, attrib_field, region_value)
        mesh = checkIntersect(g[0], mesh, x_min, 'district', district_name)
    elif type(g[0]) == type(mpoly):
        print('MultiPolygon: ', district_name)
        listPoly = list(g[0])
        for lpoly in listPoly:
            mesh = checkIntersect(lpoly, mesh, x_min, 'district', district_name)


    mpoly = 0
    poly = 0
    return mesh
#-------------------------------------------------------------------------------
'''
create geodataframe from another geodataframe. Initially, we adopted populations
'''
def create_geoseries(population, x_delta, y_delta, x_max, x_min, y_max,  y_min):
    x = x_min
    y = y_min
    ID = 0
    ID_v     = []
    COORD_v  = []
    INDEX_v  = []
    X_MAX    = []
    X_MIN    = []
    Y_MAX    = []
    Y_MIN    = []

    #we must to close polygon, it means, the last point must be equal to the first one
    while y <= y_max:
        x = x_min#
        while x <= x_max:
            s_poly = 'POLYGON (({0:.20f} {1:.20f}, {2:.20f} {1:.20f}, {2:.20f} {3:.20f}, {0:.20f} {3:.20f}, {0:.20f} {1:.20f}))'.format(x, y, x + x_delta, y + y_delta)
            ID_v.append(ID)
            COORD_v.append(s_poly)
            INDEX_v.append('unknow!')
            X_MAX.append( x + x_delta)
            X_MIN.append( x - x_delta)
            Y_MAX.append( y + y_delta)
            Y_MIN.append( y - y_delta)
            x = x + x_delta
            ID = ID + 1
            if (ID % 100) == 0:
                print('.', end = '')
        y = y + y_delta

    print('Creating dataframe')
    df=pd.DataFrame({'id':ID_v, 'geometry':COORD_v, 'district':INDEX_v, 'x_max':X_MAX, 'x_min': X_MIN, 'y_max':Y_MAX, 'y_min': Y_MIN })

    print('Creating geoseries')
    df['geometry'] = geopandas.GeoSeries.from_wkt(df['geometry'])
    gdf = geopandas.GeoDataFrame(df, geometry='geometry')
    #sprint('Saving mesh')
    #gdf.to_file("mesh.shp")
    return gdf
    #print('Saving file')


#-------------------------------------------------------------------------------
'''
input: meters
output: global respective coodinates - used to define the lattice cell size in angles
'''
def convert_latlong2meters(x, y):
    transformer = Transformer.from_crs(4326, 3857, always_xy=True)
    return transformer.transform(x, y)
'''
    outProj = Proj(init='epsg:4326') # It is equal to WSG
    inProj = Proj(init='epsg:3857') #meters

    x2,y2 = transform(inProj,outProj, x, y)
    print ("Coordenate(", x2, ",", y2, ")")
'''
#-------------------------------------------------------------------------------
'''
input: meters
output: global respective coodinates - used to define the lattice cell size in angles
'''
def convert_meters2latlong(x, y):
    transformer = Transformer.from_crs(3857, 4326, always_xy=True)
    return transformer.transform(x, y)
'''
    outProj = Proj(init='epsg:4326') # It is equal to WSG
    inProj = Proj(init='epsg:3857') #meters

    x2,y2 = transform(inProj,outProj, x, y)
    print ("Coordenate(", x2, ",", y2, ")")
'''
#-------------------------------------------------------------------------------
'''
input: polygon coordinate set
output: mins and maxs of the coordiantes
'''
def mins_and_maxs(coords):
    x, y = coords.xy
    x_lmax = max(x)
    x_lmin = min(x)
    y_lmax = max(y)
    y_lmin = min(y)
    return x_lmax, x_lmin, y_lmax, y_lmin
#-------------------------------------------------------------------------------
'''
input: geopandas dataframe with a city region
output: bounding box of the city
'''
def extrac_bounding_box(region):
    #print(geometry.boundary)
    #print(geometry.centroid)
    #print(geometry.convex_hull)
    #print(type(geometry.convex_hull))
    g = [i for i in region.geometry]

    x, y = g[0].exterior.coords.xy
    x_max = max(x)
    x_min = min(x)
    y_max = max(y)
    y_min = min(y)
    #print(len(g))
    mpoly = MultiPolygon()
    poly  = Polygon()
    for i in range(0, len(g)):
        if type(g[i]) == type(poly):
            x_lmax, x_lmin, y_lmax, y_lmin = mins_and_maxs(g[i].exterior.coords)
            x_max = max(x_max, x_lmax)
            x_min = min(x_min, x_lmin)
            y_max = max(y_max, y_lmax)
            y_min = min(y_min, y_lmin)
        elif type(g[i]) == type(mpoly):
            listPoly = list(g[i])
            for lpoly in listPoly:
                x_lmax, x_lmin, y_lmax, y_lmin = mins_and_maxs(lpoly.exterior.coords)
                x_max = max(x_max, x_lmax)
                x_min = min(x_min, x_lmin)
                y_max = max(y_max, y_lmax)
                y_min = min(y_min, y_lmin)

    return x_max, x_min, y_max, y_min

#-------------------------------------------------------------------------------
'''
p1 and p2 are polygon Coordinate
p4x is maximum value used to cal if point in or out
b2 is b value of second line
'''
def point_in_poly_faster(p1x, p1y, p2x, p2y, p4x, p3x, p3y):
    is_in = True
    #print('\t\t point_in_poly_faster:')
    # first line
    if abs(p2x - p1x) <= 1E-20 or abs(p2y - p1y) <= 1E-20:
        msg = '[ERROR] at line 75 in python script \n'
        stderr_fileno.write(msg)
        sys.exit(-1)
    else:

        a1 = (p2y - p1y) / (p2x - p1x)


    b1 = (p1y +(-p1x * a1)) * -1
    b2 = p3y

    x = (b1 + b2) / (a1)
    y = b2

    scale_x = (p2x - x) / (p2x - p1x)
    scale_y =  (p2y - y) /  (p2y - p1y)
    scale_xx = (p4x - x) / (p4x - p3x)

    if scale_x < 0 or scale_x > 1:
        is_in = False

    if scale_y < 0 or scale_y > 1:
        is_in = False

    if scale_xx < 0 or scale_xx > 1:
        is_in = False


    #print('\t point: ', x, ' ', y)
    #print('\t scale: ', scale_x, ' ', scale_y)

    return is_in


#-------------------------------------------------------------------------------
'''
Add a new attribute layer in mesh geopandas dataframa - it is another column
'''
def addAttribSetValueFromPoly(mesh, attrib_field, inter_region, region_value, x_min):

    g = [i for i in inter_region.geometry]
    mpoly = MultiPolygon()
    poly  = Polygon()
    if type(g[0]) == type(poly):
        print('Poly')
        mesh = checkIntersect(g[0], mesh, x_min, attrib_field, region_value)
    elif type(g[0]) == type(mpoly):
        print('MPoly')
        listPoly = list(g[0])
        for lpoly in listPoly:
            mesh = checkIntersect(lpoly, mesh, x_min, attrib_field, region_value)

    mpoly = 0
    poly = 0
    return mesh
'''
Add a new attribute layer in mesh geopandas dataframa - it is another column
It is used to get bus stations in the city which has several stations along the city
'''
def addAttribSetValueFromMultiPointsAABBLattice(x_g_max, x_g_min, y_g_max, y_g_min, attrib):
    for i in range(0, len(attrib)):
        df = attrib.iloc[i]
        mList = list(df.geometry)

        print(i,'/', len(attrib), '\t with: ', len(mList))
        for j in range(0, len(mList)):
            a_x, a_y = mList[j].centroid.xy
            x_p1 = a_x[0]
            y_p1 = a_y[0]



            in_side = True
            if x_p1 < x_g_min:
                in_side = False

            if x_p1 > x_g_max:
                in_side = False

            if y_p1 < y_g_min:
                in_side = False

            if y_p1 > y_g_max:
                in_side = False

            if in_side == True:
                attrib.loc[i, 'in_out'] = 1

    return attrib
'''
Add a new attribute layer in mesh geopandas dataframa - it is another column
It is used to get bus stations in the city which has several stations along the city
'''
def addAttribSetValueFromMultiPointsAABB(attribute_gdf, mesh, attib_field):
    aux_attib_field = attib_field


    for i in range(0, len(attribute_gdf)):
        df = attribute_gdf.iloc[i]
        mList = list(df.geometry)

        print(i,'/', len(attribute_gdf), '\t with: ', len(mList))
        for j in range(0, len(mList)):
            a_x, a_y = mList[j].centroid.xy
            x_p1 = a_x[0]
            y_p1 = a_y[0]
            for k in range(0, len(mesh)): #for each cell, I will check if there is or not a bus stop

                lMesh =  mesh.iloc[k]

                x_g_max = lMesh.x_max
                x_g_min = lMesh.x_min
                y_g_max = lMesh.y_max
                y_g_min = lMesh.y_min

                in_side = True
                if x_p1 < x_g_min:
                    in_side = False

                if x_p1 > x_g_max:
                    in_side = False

                if y_p1 < y_g_min:
                    in_side = False

                if y_p1 > y_g_max:
                    in_side = False

                if in_side == True:
                    value = lMesh[aux_attib_field]
                    value = value + 1
                    mesh.loc[mesh.id == lMesh.id, aux_attib_field] = value
    return mesh
#-------------------------------------------------------------------------------
'''
Add a new attribute layer in mesh geopandas dataframa - it is another column
This procedure is based on distance in global coordiante domain
'''
def addAttribSetValueFromPointsAABB(mesh, attib_field, attribute_gdf):
    #aux1 = school_jg.loc[school_jg['INEP'] == 33085951]

    #print(int(aux1.INEP))


    aux_attib_field = attib_field
    size = len(mesh)
    #s_domain = math.floor(len(school_jg) / threads)
    #https://github.com/classner/pymp/blob/master/README.md
    #with pymp.Parallel(threads) as p:
    #    for i in p.range(0, len(school_jg)):
    #        if p.thread_num == 0:
    #            print(i, '/', s_domain)
    for i in range(0, len(attribute_gdf)):
        print(i, '/', len(attribute_gdf))
        a_x, a_y = attribute_gdf.iloc[i].geometry.centroid.xy
        x_p1 = a_x[0]
        y_p1 = a_y[0]
        for k in range(0, size): #for each cell, I will check if there is or not a bus stop

            lMesh =  mesh.iloc[k]

            x_g_max = lMesh.x_max
            x_g_min = lMesh.x_min
            y_g_max = lMesh.y_max
            y_g_min = lMesh.y_min

            in_side = True
            if x_p1 < x_g_min:
                in_side = False

            if x_p1 > x_g_max:
                in_side = False

            if y_p1 < y_g_min:
                in_side = False

            if y_p1 > y_g_max:
                in_side = False

            if in_side == True:
                value = lMesh[aux_attib_field]
                value = value + 1
                mesh.loc[mesh.id == lMesh.id, aux_attib_field] = value
    return mesh
#-------------------------------------------------------------------------------
