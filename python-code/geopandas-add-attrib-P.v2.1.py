#! /home/mzamith/Apps/anaconda3/bin/python
import geopandas
import sys
from geopandas import GeoSeries
from shapely.geometry import Polygon, MultiPolygon
import ufrrjgeo
#-------------------------------------------------------------------------------
'''
Add a new attribute layer in mesh geopandas dataframa - it is another column
This procedure is based on distance in global coordiante domain
'''
def addAttribSetValueFromPointsAABBLattice( x_g_max, x_g_min, y_g_max, y_g_min, attrib):
    size = len(attrib)
    '''
    for i in range(0, size):
        attrib.loc[i, 'id'] = i
    '''
    for i in range(0, size):
        print(i, '/', size)
        a_x, a_y = attrib.iloc[i].geometry.centroid.xy
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
#-------------------------------------------------------------------------------



if __name__ == "__main__":
    print('Extrating attributes based on points v2.1')
    enco           = 'ISO-8859-1'

    shp_file_name  =  sys.argv[1]#'/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/Escolas/educ_escolasPoint.shp'
    shp_mesh_file  =  sys.argv[2]#'/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-rb/recreio-dos-bandeirantes-050.shp'
    shp_log_file   =  sys.argv[3]#'/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-rb/recreio-dos-bandeirantes-050-escolas.shp'
    newattrib      =  sys.argv[4]# 'shool' #sys.argv[4] #'school'
    #state_name     =  sys.argv[4] #'RIO DE JANEIRO'
    #newattrib = sys.argv[4] #'school'
    attrib  = geopandas.read_file(shp_file_name, encodig=enco)
    mesh    = geopandas.read_file(shp_mesh_file, encodig='utf-8')


    #mesh[newattrib] = 0
    attrib['in_out'] = 0
    attrib['id'] = 0
    x_g_max, x_g_min, y_g_max, y_g_min = ufrrjgeo.extrac_bounding_box(mesh)
    print('Global bounding box:', x_g_max, ' ', x_g_min, ' ', y_g_max, ' ', y_g_min)
    attrib = ufrrjgeo.addAttribSetValueFromPointsAABBLattice(x_g_max, x_g_min, y_g_max, y_g_min, attrib)
    attrib_tmp = attrib.loc[attrib['in_out'] == 1]
    print('Sizes: attrib:', len(attrib), ' \t attrib_tmp:', len(attrib_tmp))
    mesh[newattrib] = 0
    mesh = ufrrjgeo.addAttribSetValueFromPointsAABB(mesh, newattrib, attrib_tmp)
    mesh.to_file(shp_log_file)
    #
    #mesh = ufrrjgeo.addAttribSetValueFromPointsAABB(mesh, newattrib, attrib)
    #mesh.to_file(shp_log_file)
    #attrib_tmp.to_file('/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-demo/demo.shp')
    #for i in range(0, len(mesh)):
    #    print(mesh.iloc[i])
