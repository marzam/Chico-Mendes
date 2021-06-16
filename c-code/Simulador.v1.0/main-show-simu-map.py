#!/home/mzamith/Apps/anaconda3/bin/python
import sys
import geopandas
import matplotlib.pyplot as plt
def show_mapa_from_geodf(map, park, lake, simu):
    fig, ax = plt.subplots()
    map.plot(ax=ax, color='white', edgecolor='red')
    park.plot(ax=ax, color='white', edgecolor='blue')
    lake.plot(ax=ax, color='white', edgecolor='green')
    simu.plot(ax=ax, color='white', alpha=0.5, edgecolor='black')
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
    simu  = 'simulated/simulate-steps-3.shp'
    geo_state = geopandas.read_file(state, encodig='ISO-8859-1')
    geo_lake = geopandas.read_file(lake, encodig='ISO-8859-1')
    geo_park = geopandas.read_file(park, encodig='ISO-8859-1')
    geo_simu = geopandas.read_file(simu, encodig='ISO-8859-1')

    geo_city = geo_state.loc[geo_state['municipio'] == 'RIO DE JANEIRO']
    geo_pCM  = geo_park.loc[geo_park['id'] == 897]
    geo_lCM  = geo_lake.loc[geo_lake['id'] == 957]
    #print(geo_pCM)
    show_mapa_from_geodf(geo_city, geo_pCM, geo_lCM, geo_simu)
