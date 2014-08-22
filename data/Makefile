
database: db_drop db_create db_roads db_roadnames db_boundaries db_union_length

# psql -d tiger -q -f roads.sql
# psql -d tiger -q -f roadnames.sql
# # ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=tiger" "http://services2.arcgis.com/1gVyYKfYgW5Nxb1V/ArcGIS/rest/services/MesaAzCouncilDistricts/FeatureServer/0/query?where=objectid+%3D+objectid&outfields=*&f=json" OGRGeoJSON -nln "mesa_boundaries" -t_srs "EPSG:4269"
# psql -d tiger -q -f mesa_boundaries.sql
# psql -d tiger -a -f postgis_union_length.sql

db_drop:
	psql -c "DROP DATABASE IF EXISTS tiger"

db_create:
	createdb tiger
	psql -d tiger -c "CREATE EXTENSION postgis;"

db_roads: roads.sql
	psql -d tiger -q -f roads.sql

db_roadnames: roadnames.sql
	psql -d tiger -q -f roadnames.sql

db_boundaries: mesa_boundaries.sql
	psql -d tiger -q -f mesa_boundaries.sql

db_union_length:
	psql -d tiger -a -f postgis_union_length.sql


tl_2013_04013_edges2.shp:
	wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/EDGES/tl_2013_04013_edges.zip
	unzip tl_2013_04013_edges.zip
	SHAPE_ENCODING="ISO-8859-1" && ogr2ogr tl_2013_04013_edges2.shp tl_2013_04013_edges.shp -lco ENCODING=UTF-8

roads.sql: tl_2013_04013_edges2.shp
	shp2pgsql -D -W "LATIN1" -s 4269 tl_2013_04013_edges2.shp roads > roads.sql


#get maricopa county feature names from us census:
tl_2013_04013_featnames.dbf:
	wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/FEATNAMES/tl_2013_04013_featnames.zip
	unzip tl_2013_04013_featnames.zip

roadnames.sql: tl_2013_04013_featnames.dbf
	@echo "You can ignore the following notice about a missing tl_2013_04013_featnames.shp; we don't need it"
	shp2pgsql -D -W "LATIN1" -s 4269 tl_2013_04013_featnames roadnames > roadnames.sql

# Mesa: 16000US0446000
PLACEID := 16000US0446000

mesa_boundaries.sql:
	rm -f mesa_boundaries.shp #in case it existed already
	# ogr2ogr -f 'ESRI Shapefile' mesa_boundaries.shp "http://services2.arcgis.com/1gVyYKfYgW5Nxb1V/ArcGIS/rest/services/MesaAzCouncilDistricts/FeatureServer/2/query?where=objectid+%3D+objectid&outfields=*&f=json" OGRGeoJSON
	ogr2ogr -f 'ESRI Shapefile' mesa_boundaries.shp "http://api.censusreporter.org/1.0/geo/tiger2012/$(PLACEID)?geom=true"
	shp2pgsql -D -W "LATIN1" -s 4269 mesa_boundaries.shp > mesa_boundaries.sql


clean:
	git ls-files -o | xargs rm

