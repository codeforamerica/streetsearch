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
	make -f data/Makefile

find_place_id:
	curl -G -v "http://api.censusreporter.org/1.0/geo/search" --data-urlencode "q=${PLACENAME}"
	@printf "\n pass the select full_geoid as a parameter to find_tiger_line_id \n e.g. make find_tiger_line_id PLACEID=\"16000US3651000\"\n"

#get geo-id of parent
find_tiger_line_id:
	curl -G -v "http://api.censusreporter.org/1.0/geo/tiger2012/${PLACEID}/parents"
	@printf "\n the last 6 digits of the GEOID field \n at level 50 or, the county, are the tiger line id \n pass these as an argument \n e.g. make database TIGERID=\"36061\" PLACEID=\"16000US3651000\"\n"
