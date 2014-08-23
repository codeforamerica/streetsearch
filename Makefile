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