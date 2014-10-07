
#PSQL = psql $(DB)
# DB = heroku pg:psql
DB = -d tiger
HEROKU = postgres://qllufmrlpjjoom:QUrv1bd2dEn6wU5SFipP7EL5xB@ec2-54-225-103-9.compute-1.amazonaws.com:5432/d584tj8u3bfgga

#tiger line census name
#NYC = 36061
#MESA = 04013
TIGERID = 36061

#place id for city boundary data
# Mesa: 16000US0446000
# NYC: 16000US3651000
PLACEID = 16000US3651000

# make database PSQL="heroku pg:psql"

database: db_dev_drop db_dev_create tables

tables: db_roads db_roadnames db_boundaries db_group_union

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

db_roads: roads${TIGERID}.sql
	psql $(DB) -q -f roads${TIGERID}.sql

db_roadnames: roadnames${TIGERID}.sql
	psql $(DB) -q -f roadnames${TIGERID}.sql

db_boundaries: boundaries${PLACEID}.sql
	psql $(DB) -q -f boundaries${PLACEID}.sql

db_group_union:
	psql $(DB) -a -f data/union_group.sql

#tiger line census name
#NYC = 36061


tl_2013_${TIGERID}_edges2.shp:
	wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/EDGES/tl_2013_${TIGERID}_edges.zip
	unzip tl_2013_${TIGERID}_edges.zip
	SHAPE_ENCODING="ISO-8859-1" && ogr2ogr tl_2013_${TIGERID}_edges2.shp tl_2013_${TIGERID}_edges.shp -lco ENCODING=UTF-8

roads${TIGERID}.sql: tl_2013_${TIGERID}_edges2.shp
	shp2pgsql -D -W "LATIN1" -s 4269 tl_2013_${TIGERID}_edges2.shp roads${TIGERID} > roads${TIGERID}.sql

#get maricopa county feature names from us census:
tl_2013_${TIGERID}_featnames.dbf:
	wget ftp://ftp2.census.gov/geo/tiger/TIGER2013/FEATNAMES/tl_2013_${TIGERID}_featnames.zip
	unzip tl_2013_${TIGERID}_featnames.zip

roadnames${TIGERID}.sql: tl_2013_${TIGERID}_featnames.dbf
	@echo "You can ignore the following notice about a missing tl_2013_${TIGERID}_featnames.shp; we don't need it"
	shp2pgsql -D -W "LATIN1" -s 4269 tl_2013_${TIGERID}_featnames roadnames${TIGERID} > roadnames${TIGERID}.sql

boundaries${PLACEID}.sql:
	rm -f boundaries${PLACEID}.shp #in case it existed already
	# ogr2ogr -f 'ESRI Shapefile' mesa_boundaries.shp "http://services2.arcgis.com/1gVyYKfYgW5Nxb1V/ArcGIS/rest/services/MesaAzCouncilDistricts/FeatureServer/2/query?where=objectid+%3D+objectid&outfields=*&f=json" OGRGeoJSON
	ogr2ogr -f 'ESRI Shapefile' boundaries${PLACEID}.shp "http://api.censusreporter.org/1.0/geo/tiger2012/$(PLACEID)?geom=true"
	shp2pgsql -D -W "LATIN1" -s 4269 boundaries${PLACEID}.shp boundaries${PLACEID} > boundaries${PLACEID}.sql

clean:
	git ls-files -o | xargs rm
