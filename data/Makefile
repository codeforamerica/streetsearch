
database: roads.sql roadnames.sql mesa_boundaries.sql
	psql -c "DROP DATABASE IF EXISTS tiger"
	createdb tiger
	psql -d tiger -c "CREATE EXTENSION postgis;"
	psql -d tiger -q -f roads.sql
	psql -d tiger -q -f roadnames.sql
	# ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=tiger" "http://services2.arcgis.com/1gVyYKfYgW5Nxb1V/ArcGIS/rest/services/MesaAzCouncilDistricts/FeatureServer/0/query?where=objectid+%3D+objectid&outfields=*&f=json" OGRGeoJSON -nln "mesa_boundaries" -t_srs "EPSG:4269"
	psql -d tiger -q -f mesa_boundaries.sql
	psql -d tiger -a -f postgis_union_length.sql

test:
	psql -d tiger -a -f postgis_union_length.sql


tl_2013_04013_edges2.shp:
	wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/EDGES/tl_2013_04013_edges.zip
	unzip tl_2013_04013_edges.zip
	SHAPE_ENCODING="ISO-8859-1" && ogr2ogr tl_2013_04013_edges2.shp tl_2013_04013_edges.shp -lco ENCODING=UTF-8

roads.sql: tl_2013_04013_edges2.shp
	shp2pgsql -dD -W "LATIN1" -s 4269 tl_2013_04013_edges2.shp roads > roads.sql

#get maricopa county feature names from us census:
tl_2013_04013_featnames.dbf:
	wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/FEATNAMES/tl_2013_04013_featnames.zip
	unzip tl_2013_04013_featnames.zip

roadnames.sql: tl_2013_04013_featnames.dbf
	shp2pgsql -dD -W "LATIN1" -s 4269 tl_2013_04013_featnames.shp roadnames > roadnames.sql

mesa_boundaries.sql:
	rm -f mesa_boundaries.shp #in case it existed already
	# ogr2ogr -f 'ESRI Shapefile' mesa_boundaries.shp "http://services2.arcgis.com/1gVyYKfYgW5Nxb1V/ArcGIS/rest/services/MesaAzCouncilDistricts/FeatureServer/2/query?where=objectid+%3D+objectid&outfields=*&f=json" OGRGeoJSON
	ogr2ogr -f 'ESRI Shapefile' mesa_boundaries.shp "http://api.censusreporter.org/1.0/geo/tiger2012/16000US0446000?geom=true"
	shp2pgsql -dD -W "LATIN1" -s 4269 mesa_boundaries.shp > mesa_boundaries.sql


clean:
	git ls-files -o | xargs rm

