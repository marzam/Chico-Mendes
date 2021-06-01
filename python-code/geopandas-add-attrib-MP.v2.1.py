#! /home/mzamith/Apps/anaconda3/bin/python
import geopandas
import sys
from geopandas import GeoSeries
from shapely.geometry import Polygon, MultiPolygon
import ufrrjgeo
#-------------------------------------------------------------------------------
#def addAttribSetValueFromMultiPoints(element, mesh, x_min, attib_field):
if __name__ == "__main__":
    print('Extrating attributes based on points')
    enco           = 'ISO-8859-1'

    #shp_file_name  = '/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/PontosOnibus/trans_onibus_por_embarque.shp'
    newattrib = 'bus_s'
    shp_file_name  =  sys.argv[1] #'/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/Escolas/educ_escolasPoint.shp'
    shp_mesh_file  =  sys.argv[2] #'/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp/JARDIM-GUANABARA-050.shp'
    shp_log_file   =  sys.argv[3] #'/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp/JARDIM-GUANABARA-050_ESCOLAS.shp'
    newattrib = sys.argv[4] #'school'

#    attrib = geopandas.read_file(shp_file_name, encodig=enco)
    attrib = geopandas.read_file(shp_file_name, encodig=enco)
    mesh   = geopandas.read_file(shp_mesh_file, encodig='utf-8')
    attrib['in_out'] = 0
    x_g_max, x_g_min, y_g_max, y_g_min = ufrrjgeo.extrac_bounding_box(mesh)
    print('Global bounding box:', x_g_max, ' ', x_g_min, ' ', y_g_max, ' ', y_g_min)
    attrib = ufrrjgeo.addAttribSetValueFromMultiPointsAABBLattice(x_g_max, x_g_min, y_g_max, y_g_min, attrib)
    attrib_tmp = attrib.loc[attrib['in_out'] == 1]

    print('Sizes: attrib:', len(attrib), ' \t attrib_tmp:', len(attrib_tmp))
    mesh[newattrib] = 0
    mesh = ufrrjgeo.addAttribSetValueFromMultiPointsAABB(attrib_tmp, mesh, newattrib)

    mesh.to_file(shp_log_file)
