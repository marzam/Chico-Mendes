We created several lattice, one for each attribute used. It was a better option
than just one mesh, in special case of bus stations which takes several hours to
pre-processing.
The scripts are:
geopandas-add-attrib-MP.v2.1.py -> creates a lattice based on geodataframa with multipoints as bus stations
geopandas-add-attrib-P.v2.1.py -> creates a lattice based on geodataframa with points as schools and hospitals
geopandas-create-mesh-from-neighborhood.v2.0.py -> define a mesh based on neighborhood
geopandas-createMesh.py
geopandas-export-ChicoMendes-data.py -> create meshes based on Chico Mendes Park

* Demo scripts so that I can learn about GeoDataFrame

geopandas-getCoord.py -
main.py
point-in-poly-exemplo.py
script-jg.py
script.py
script-recreio.py
script-recreio.tmp.py
ufrrjgeo.py
