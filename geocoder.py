import psycopg2
import pprint
import string
import os

# success is returning:
# West Jerome Avenue
# Country Club Drive
# Baseline Road

is_production = False

pp = pprint.PrettyPrinter(indent=4)

suffixes = 'Ave Blvd Cir Ct Dr Ln Pl Rd St Way'.split()

prefix = {'North':'N','South':'S','East':'E','West':'W'}
abbr = {'Avenue': 'Ave', 'Boulevard': 'Blvd', 'Circle': 'Cir', 'Court': 'Ct', 'Drive': 'Dr', 'Lane':'Ln', 'Place': 'Pl','Road':'Rd','Street':'St','Way':'Way'}

# TODO - also look for addresses (numbers)
# find and return all roadnames that match test_string in the database.
# test_string: a string containing natural language and potentially some addresses
def find_in_database(test_string):
	# print the connection string we will use to connect
	#print "Connecting to database\n	->%s" % (connection_string)

	global is_production
	if is_production:
		# Configuration settings may vary from server to server:
		print os.environ["DATABASE_URL"]
		username = os.environ["DATABASE_URL"].split(":")[1].replace("//","")
		password = os.environ["DATABASE_URL"].split(":")[2].split("@")[0]
		host = os.environ["DATABASE_URL"].split(":")[2].split("@")[1].split("/")[0]
		dbname = os.environ["DATABASE_URL"].split(":")[3].split("/")[1]
		dbport = os.environ["DATABASE_URL"].split(":")[3].split("/")[0]
		print "database name: " + dbname
		db_conn = psycopg2.connect(dbname=dbname, user=username, password=password, host=host,port=dbport)
	else:
		db_conn = psycopg2.connect(dbname='tiger', host='localhost', port='5432')


	cursor = db_conn.cursor()
	print "Connected!\n"

	queryd = "SELECT * FROM mesaroads limit 1;"
	cursor.execute(queryd)
	records = cursor.fetchall()
	print records

	# Always use this query:
	query = "SELECT fullname, ST_ASGeoJSON(geom) FROM mesaroads WHERE fullname ~ '" + test_string + "'"
	cursor.execute(query);

	# retrieve the records from the database
	records = cursor.fetchall()
	cursor.close()
	db_conn.close()

	return records


# seek backwards in sentence from the tail that begins at index i
# returns a list of 0 or more locations.
# the locations are based on the fragment at the given index in the text, and
# can be found in the tiger/roads database.
#
# text: an array of words (a sentence broken up on whitespace)
# fragment: a string of text that already matches (e.g. "Rd")
# index: the index of the fragment within text
# matches: list of matches we already found that we'd like to refine
def seek_backwards(text, fragment, index, matches):
	print fragment
	if index == 0:
		return matches
	print index
	prev_index = index - 1

	this_word = text[prev_index]
	print this_word
	if this_word in prefix.keys():
		this_word = prefix[this_word]

	test_string = this_word + ' ' + fragment
	print test_string
	# get locations = matches for p + suffix in roads database/name column
	new_matches = find_in_database(test_string)
	print "matches"
	print new_matches
	if len(new_matches) == 0:
		return matches # stick w/ old results
	elif len(new_matches) == 1:
		return new_matches
	else:
		return seek_backwards(text, test_string, prev_index, new_matches) 

# until end of sentence:

	# get word
	# does suffixes contain word?

	# if no, advance to next word

	# if yes, get previous word P 

	# get locations = matches for p + suffix in roads database/name column

	# if locations.number = 1 done
	# if locations.number = 0 then advance to next word 

	# if locations.number > 1 
	# 	get previous word p' 
	# 	locations2 = matches for p' + p + suffix 
	# 	if locations2.length = 1 done
	# 	if locations2.length = 0, return locations
	# 	elsif locations2.length > 1

# matches will be all the sentence fragments ("Alma School Rd", "295 8th Street") which match TIGER-based locations
def geocode_text(production, sentence):
	global is_production
	is_production = production
	sentence = sentence.encode('utf8')
	sentence = sentence.translate(string.maketrans("",""), string.punctuation).split()

	all_matches = []
	for i, word in enumerate(sentence):
		if word in abbr.keys():
			word = abbr[word]
			#print word
		if word in suffixes:
			print "seeking backwards from " + word + " at index: " + str(i)
			these_matches = seek_backwards(sentence, word, i, [])
			print these_matches
			if these_matches:
				all_matches += these_matches
	return all_matches
	print all_matches
# now do something with all_matches.
