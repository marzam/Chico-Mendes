#! /home/mzamith/Apps/anaconda3/bin/python
#./geopandas-create-mesh-from-neighborhood.v2.0.py /home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/bairros_populacao.shp  RIO\ DE\ JANEIRO JARDIM\ GUANABARA shp/JARDIM-GUANABARA-050.shp 50
#./geopandas-add-attrib.v2.0.py /home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/Escolas/educ_escolasPoint.shp shp/JARDIM-GUANABARA-050.shp shp/JARDIM-GUANABARA-050_ESCOLAS.shp RIO\ DE\ JANEIRO JARDIM\ GUANABARA Bairro school
# Não tem o campo bairro ?!?!!! usar o todo sempre
#./geopandas-add-attrib.v2.0.py /home/mzamith/Documents/Develop/qgis-3/RJ-01-exemplos.py/saude_oss/saude_oss.shp shp/JARDIM-GUANABARA-050.shp shp/JARDIM-GUANABARA-050_SAUDE.shp RIO\ DE\ JANEIRO JARDIM\ GUANABARA Bairro health
from pathlib import Path
import os
#inloco MP site data
population   = '../Populacao/bairros_populacao.shp'
schools      = '../Escolas/educ_escolasPoint.shp'
health       = '../saude_oss/saude_oss.shp'
bus_line     = '../PontosOnibus/trans_onibus_por_embarque.shp'
#config.
city             = 'RIO\ DE\ JANEIRO'
neighborhood     = 'RECREIO\ DOS\ BANDEIRANTES'
discretization   = 50 #50 meters
output_dir   = 'shp-rb/'
output_mesh  = 'recreio-dos-bandeirantes-050.shp'
#output file sabed on output_dic
output_mesh_school  = 'recreio-dos-bandeirantes-050-school.shp'
output_mesh_health  = 'recreio-dos-bandeirantes-050-health.shp'
output_mesh_bus     = 'recreio-dos-bandeirantes-050-bus.shp'
#geodataframe fields
field_school        = 'school'
field_healt         = 'health'
field_bus           = 'bus'

log_mesh_std            = 'log/rb-mesh-std.log'
log_mesh_err            = 'log/rb-mesh-err.log'

log_school_std          = 'log/rb-school-std.log'
log_health_std          = 'log/rb-school-std.log'
log_bus_std             = 'log/rb-bus-std.log'

log_school_err          = 'log/rb-school-err.log'
log_health_err          = 'log/rb-school-err.log'
log_bus_err             = 'log/rb-bus-err.log'

print('Data pre-processing step')
Path(output_dir).mkdir(parents=True, exist_ok=True)
#command = './geopandas-create-mesh-from-neighborhood.v2.0.py {} {} {} {}{} {} '.format(population, city, neighborhood, output_dir, output_mesh, discretization, log_mesh_std, log_mesh_err)
command = './geopandas-create-mesh-from-neighborhood.v2.0.py {} {} {} {}{} {} {} {}'.format(population, city, neighborhood, output_dir, output_mesh, discretization, log_mesh_std, log_mesh_err)
print(command)
os.system(command)

#command = './geopandas-add-attrib-P.v2.0.py {} {}{} {}{} {} > {} 2> {} &'.format(schools, output_dir, output_mesh, output_dir, output_mesh_school, field_school, log_school_std, log_school_err)
#command = './geopandas-add-attrib-P.v2.1.py {} {}{} {}{} {} '.format(schools, output_dir, output_mesh, output_dir, output_mesh_school, field_school, log_school_std, log_school_err)
#os.system(command)

#command = './geopandas-add-attrib-P.v2.0.py {} {}{} {}{} {} > {} 2> {} &'.format(health, output_dir, output_mesh, output_dir, output_mesh_health, field_healt, log_health_std, log_health_err)
#command = './geopandas-add-attrib-P.v2.1.py {} {}{} {}{} {} '.format(health, output_dir, output_mesh, output_dir, output_mesh_health, field_healt, log_health_std, log_health_err)
#os.system(command)

#command = './geopandas-add-attrib-MP.v2.0.py {} {}{} {}{} {} > {} 2> {} &'.format(bus_line, output_dir, output_mesh, output_dir, output_mesh_bus, field_bus, log_bus_std, log_bus_err)
#command = './geopandas-add-attrib-MP.v2.1.py {} {}{} {}{} {} '.format(bus_line, output_dir, output_mesh, output_dir, output_mesh_bus, field_bus, log_bus_std, log_bus_err)
#os.system(command)
#fazer do ponto de ônibus
