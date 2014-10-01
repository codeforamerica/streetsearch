#get maricopa county roads from us census:
wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/EDGES/tl_2013_04013_edges.zip
unzip tl_2013_04013_edges.zip

export SHAPE_ENCODING="ISO-8859-1"
ogr2ogr tl_2013_04013_edges2.shp tl_2013_04013_edges.shp -lco ENCODING=UTF-8

createdb tiger
psql -d tiger -c "CREATE EXTENSION postgis;"

#import to postgis
#shp2pgsql tl_2013_04013_roads.shp roads > roads.sql
shp2pgsql -W "LATIN1" -s 4269 tl_2013_04013_edges2.shp roads > roads.sql

#clean up
#rm tl_2013_04013_edges*

psql -d tiger -f roads.sql

#get maricopa county feature names from us census:
wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/FEATNAMES/tl_2013_04013_featnames.zip
unzip tl_2013_04013_featnames.zip

# FIGURE OUT HOW TO get feature names dbf in postgres WITH ogr2ogr
# import to postgis
# shp2pgsql tl_2013_04013_roads.shp roads > roads.sql
# shp2pgsql -W "LATIN1" tl_2013_04013_featnames.shp roadnames > roadnames.sql
#ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=tiger" tl_2013_04013_featnames.dbf -nln "featnames" -lco ENCODING=UTF-8

shp2pgsql -W "LATIN1" tl_2013_04013_featnames.shp roadnames > roadnames.sql

psql -d tiger -f roadnames.sql

#clean up
rm tl_2013_04013_featnames*

#ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=tigert" sometable.dbf -nln "sometable"

ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=tiger" "http://services2.arcgis.com/1gVyYKfYgW5Nxb1V/ArcGIS/rest/services/MesaAzCouncilDistricts/FeatureServer/0/query?where=objectid+%3D+objectid&outfields=*&f=json" OGRGeoJSON -nln "mesa_boundaries" -t_srs "EPSG:4269"

psql -d tiger -a -f postgis_union_length.sql

#get geo for place
http://api.censusreporter.org/1.0/geo/tiger2012/16000US3651000?geom=true

#search for geo id for name
http://api.censusreporter.org/1.0/geo/search?q=New%20York&sumlevs=010,020,030,040,050,060,160,250,310,500,610,620,860,950,960,970
