
#PSQL = psql $(DB)
# DB = heroku pg:psql
DB = -d tiger
HEROKU = postgres://qllufmrlpjjoom:QUrv1bd2dEn6wU5SFipP7EL5xB@ec2-54-225-103-9.compute-1.amazonaws.com:5432/d584tj8u3bfgga

# make database PSQL="heroku pg:psql"

database: db_dev_drop db_dev_create tables

tables: db_roads db_roadnames db_boundaries db_union_length

# database_stage:
	# make DB=$(HEROKU) _database_heroku

# _database_heroku: db_stage_drop tables

#pg_dump -Fc --no-acl --no-owner -h localhost tiger > tiger.dump
#HEROKU_POSTGRESQL_MAGENTA
database_push: database
	 heroku pg:reset --confirm findlines-staging DATABASE_URL
	 heroku pg:push tiger DATABASE_URL --app findlines-staging


# psql $(DB) -q -f roads.sql
# psql $(DB) -q -f roadnames.sql
# # ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=tiger" "http://services2.arcgis.com/1gVyYKfYgW5Nxb1V/ArcGIS/rest/services/MesaAzCouncilDistricts/FeatureServer/0/query?where=objectid+%3D+objectid&outfields=*&f=json" OGRGeoJSON -nln "mesa_boundaries" -t_srs "EPSG:4269"
# psql $(DB) -q -f mesa_boundaries.sql
# psql $(DB) -a -f postgis_union_length.sql

# TODO: Handle drop/create differently on heroku than localhost.

db_dev_drop:
	psql -c "DROP DATABASE IF EXISTS tiger"
	psql -c "DROP EXTENSION IF EXISTS postgis"

db_stage_drop:
	 heroku pg:reset --confirm findlines-staging DATABASE_URL


db_dev_create:
	psql -c "CREATE DATABASE tiger" #createdb tiger
	psql $(DB) -c "CREATE EXTENSION postgis;"

db_stage_create:
	# nothing to do here.

db_roads: roads.sql
	psql $(DB) -q -f roads.sql

db_roadnames: roadnames.sql
	psql $(DB) -q -f roadnames.sql

db_boundaries: mesa_boundaries.sql
	psql $(DB) -q -f mesa_boundaries.sql

db_union_length:
	psql $(DB) -a -f data/postgis_union_length.sql


tl_2013_36061_edges2.shp:
	wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/EDGES/tl_2013_36061_edges.zip
	unzip tl_2013_36061_edges.zip
	SHAPE_ENCODING="ISO-8859-1" && ogr2ogr tl_2013_36061_edges2.shp tl_2013_36061_edges.shp -lco ENCODING=UTF-8

roads.sql: tl_2013_36061_edges2.shp
	shp2pgsql -D -W "LATIN1" -s 4269 tl_2013_36061_edges2.shp roads > roads.sql


#get maricopa county feature names from us census:
tl_2013_36061_featnames.dbf:
	wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/FEATNAMES/tl_2013_36061_featnames.zip
	unzip tl_2013_36061_featnames.zip

roadnames.sql: tl_2013_36061_featnames.dbf
	@echo "You can ignore the following notice about a missing tl_2013_36061_featnames.shp; we don't need it"
	shp2pgsql -D -W "LATIN1" -s 4269 tl_2013_36061_featnames roadnames > roadnames.sql

# Mesa: 16000US0446000
# NYC: 16000US3651000
PLACEID := 16000US3651000

mesa_boundaries.sql:
	rm -f mesa_boundaries.shp #in case it existed already
	# ogr2ogr -f 'ESRI Shapefile' mesa_boundaries.shp "http://services2.arcgis.com/1gVyYKfYgW5Nxb1V/ArcGIS/rest/services/MesaAzCouncilDistricts/FeatureServer/2/query?where=objectid+%3D+objectid&outfields=*&f=json" OGRGeoJSON
	ogr2ogr -f 'ESRI Shapefile' mesa_boundaries.shp "http://api.censusreporter.org/1.0/geo/tiger2012/$(PLACEID)?geom=true"
	shp2pgsql -D -W "LATIN1" -s 4269 mesa_boundaries.shp > mesa_boundaries.sql

clean:
	git ls-files -o | xargs rm
