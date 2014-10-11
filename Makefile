# Run this makefile from the root of the git repo.

TEST_TEXT="fileupload=Z14-026 (District 3) 610 West Jerome Avenue. Located west of Country Club Drive and north of Baseline Road (1.78± acres). Site Plan Modification and modification of the existing BIZ overlay within an LI zoning district. This request will allow the development of a healthcare facility. Richard Clutter, EMC2 Architects, applicant; Bill Timmons, Hacienda Healthcare, owner. Staff Recommendation: Approval with Conditions P&Z Board Recommendation: Approval with Conditions (Vote: 5-0-1, Absent: Boardmember Arnett, Abstains: Vice Chair Coons)"

SERVER = localhost
PORT = 5000

run_server:
	python server.py

debug_server:
	export DEBUG=true && make run_server

run_test:
	 curl --data-urlencode $(TEST_TEXT) $(SERVER):$(PORT)

test_server:
	 make run_test SERVER=findlines-staging.herokuapp.com PORT=80

database:
	make -f data/Makefile.Tiger

tiger_tables:
	make tables -f data/Makefile.Tiger

metro_tables:
	make tables -f data/Makefile.Metro

find_place_id:
	curl -G -v "http://api.censusreporter.org/1.0/geo/search" --data-urlencode "q=${PLACENAME}"
	@printf "\n pass the select full_geoid as a parameter to find_tiger_line_id \n e.g. make find_tiger_line_id PLACEID=\"16000US3651000\"\n"

#get geo-id of parent
find_tiger_line_id:
	curl -G -v "http://api.censusreporter.org/1.0/geo/tiger2012/${PLACEID}/parents"
	@printf "\n the last 5 digits of the GEOID field \n at level 50 or, the county, are the tiger line id \n pass these as an argument \n e.g. make tables TIGERID=\"36061\" PLACEID=\"16000US3651000\"\n"

sample_cities:
	make tiger_tables TIGERID="06075" PLACEID="16000US0667000" #san francisco city
	make tiger_tables TIGERID="11001" PLACEID="16000US1150000" #dc - dc
	make tiger_tables TIGERID="17031" PLACEID="16000US1714000" #chicago-cook county
	make tiger_tables TIGERID="36061" PLACEID="16000US3651000" #nyc - manhattan
	make tiger_tables TIGERID="41051" PLACEID="16000US4159000" #portland - multinomah county
	make tiger_tables TIGERID="48113" PLACEID="16000US4819000" #dallas - dallas county

push_table_heroku:
	pg_dump tiger -f ${TABLENAME}.sql --table ${TABLENAME}
	cat ${TABLENAME}.sql | heroku pg:psql --app findlines-staging