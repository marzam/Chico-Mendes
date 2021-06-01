#! /home/mzamith/Apps/anaconda3/bin/python
import geopandas
import sys
from geopandas import GeoSeries
from shapely.geometry import Polygon, MultiPolygon

'''
Add a new attribute layer in mesh geopandas dataframa - it is another column
This procedure is based on distance in global coordiante domain
'''
def addAttribSetValueFromMultiPointsAABB(mesh, attib_field, school_jg):
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
    for i in range(0, len(school_jg)):
        print(i)
        a_x, a_y = school_jg.iloc[i].geometry.centroid.xy
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


if __name__ == "__main__":
    print('Demo')


    shp_file_name  = '/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/Escolas/educ_escolasPoint.shp'
    shp_mesh_file  = '/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-demo/JARDIM-GUANABARA-050.shp'
    shp_log_file   = '/home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/python-code/shp-demo/JARDIM-GUANABARA-050_ESCOLAS.shp'
    enco           = 'ISO-8859-1'
    state_name     = 'RIO DE JANEIRO'
    district_name  = 'JARDIM GUANABARA'
    attrib_name    = 'Bairro'
    school = geopandas.read_file(shp_file_name, encodig=enco)
    mesh   = geopandas.read_file(shp_mesh_file, encodig='utf-8')
    school_jg = school.loc[school[attrib_name] == district_name]

    mesh['school'] = 0
    #print(school_jg.geometry.centroid)
    school_list = list(school_jg.geometry)

    mesh = addAttribSetValueFromMultiPointsAABB(mesh, 'school', school_jg)
    mesh.to_file(shp_log_file)
    #for i in range(0, len(mesh)):
    #    print(mesh.iloc[i])
