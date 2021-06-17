#!/home/mzamith/Apps/anaconda3/bin/python
import sys
import geopandas
from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt
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

def show_mapa_from_geodf(map, park, lake, simu):
    fig, ax = plt.subplots()
    map.plot(ax=ax, color='white', edgecolor='red')
    park.plot(ax=ax, color='white', edgecolor='blue')
    lake.plot(ax=ax, color='white', edgecolor='green')
    simu.plot(ax=ax, color='white', alpha=0.5, edgecolor='black')
    #xlim = ([country_boundary_us.total_bounds[0],  country_boundary_us.total_bounds[2]])
    #ylim = ([country_boundary_us.total_bounds[1],  country_boundary_us.total_bounds[3]])

    x_max, x_min, y_max, y_min = extrac_bounding_box(park)
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    plt.show()
    #fig, ax = plt.subplots(1, 1)
    #ax = region.plot(color='white', edgecolor='red')
    #ax = region.plot(column='populacao0', ax=ax, legend=True)
    #plt.show()

if __name__ == "__main__":
    print('Exibindo resultado da simulação')
    state = '../../Populacao/bairros_populacao.shp'
    lake  = '../../Lagos-Lagoa/amb_app_lagoas_25k_inea.shp'
    park  = '../../Unidade-Conservacao/amb_ucs.shp'
    simu  = 'simulated/simulate-steps-4.shp'
    geo_state = geopandas.read_file(state, encodig='ISO-8859-1')
    geo_lake = geopandas.read_file(lake, encodig='ISO-8859-1')
    geo_park = geopandas.read_file(park, encodig='ISO-8859-1')
    geo_simu = geopandas.read_file(simu, encodig='ISO-8859-1')

    geo_city = geo_state.loc[geo_state['municipio'] == 'RIO DE JANEIRO']
    geo_pCM  = geo_park.loc[geo_park['id'] == 897]
    geo_lCM  = geo_lake.loc[geo_lake['id'] == 957]
    print(geo_simu)
    show_mapa_from_geodf(geo_city, geo_pCM, geo_lCM, geo_simu)
