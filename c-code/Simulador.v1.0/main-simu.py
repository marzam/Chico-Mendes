#!/home/mzamith/Apps/anaconda3/bin/python
import sys
import cppyy
cppyy.include('CellularAutomata.hpp')
#cppyy.add_include_path('/home/mzamith/Documents/Projetos/T-UFRRJ/Traffic-Model-CA++/release-05/cpp')
cppyy.load_library('liboccupCA.so')
from cppyy.gbl import CellularAutomata
import geopandas

if __name__ == "__main__":
    print('Simulação')
    width  = 278
    height = 120
    steps  = 4
    outputfile  = 'simulated/simulate-steps-{}.shp'.format(steps)


    ca = CellularAutomata()
    dir      = '/home/mzamith/Documents/Develop/qgis-3/RJ-01-ChicoMendes.py/RecreioBandeirates/'
    lattice  = 'recreio-dos-bandeirantes-050.shp'
    #output file sabed on output_dic
    lattice_school  = 'recreio-dos-bandeirantes-050-escolas.shp'
    lattice_health  = 'recreio-dos-bandeirantes-050-health.shp'
    lattice_bus     = 'recreio-dos-bandeirantes-050-bus.shp'
    lattice_CM      = 'chico-mendes-malha-050.shp'
    print('\t Loading data')
    g_lattice = geopandas.read_file(dir + lattice, encodig='utf8')
    g_school  = geopandas.read_file(dir + lattice_school, encodig='utf8')
    g_health  = geopandas.read_file(dir + lattice_health, encodig='utf8')
    g_bus     = geopandas.read_file(dir + lattice_bus, encodig='utf8')
    g_ChicoM  = geopandas.read_file(dir + lattice_CM, encodig='utf8')
    #g_ChicoMR = geopandas.read_file(dir + lattice_CM, encodig='utf8')
    print('\t\t Lattice: ', len(g_lattice))
    print('\t\t  School: ', len(g_school))
    print('\t\t     Bus: ', len(g_bus))
    print('\t\t  Health: ', len(g_health))
    print('\t\t Chico M: ', len(g_ChicoM))
    size = len(g_lattice)
    ca.setLattice(width, height)
    s_school = 0
    s_health = 0
    s_bus = 0
    '''
    print(width, ' ', height, ' ', size)
    print(g_lattice.columns.values)
    g_lattice['occupied'] = 0
    print(g_lattice.columns.values)
    '''
    g_lattice['occupied'] = 0
    for i in range(0, size):
        id = g_lattice.iloc[i].id
        x, y = g_lattice.iloc[i].geometry.centroid.xy

        i_y = int(id / width)
        i_x = int(id % width)

        change = False
        bus = g_bus.iloc[i].bus
        health = g_health.iloc[i].health
        school = g_school.iloc[i].shool
        state  = g_ChicoM.iloc[i].states
        if state == 0:
            change = True
        ca.setData(i_x, i_y, int(id), int(bus), int(health), int(school), x[0], y[0], int(state), change)

    print('\t\t buildList')
    ca.buildList()
    print('\t\t setWeightSuitability')
    ca.setWeightSuitability()
    for i in range(0, steps):
        print('\t\t\t update - step ', steps)
        ca.update()

    for i in range(0, ca.getCellSimulatedSize()):
        index = ca.getCellSimulated(i);
        s = ca.getState(index);
        g_lattice.loc[index, 'occupied'] = s


    tmp = g_lattice.loc[g_lattice['occupied'] == 1]
    tmp.to_file(outputfile)
    print(outputfile, ' saved')
