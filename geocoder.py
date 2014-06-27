# from nltk.util import ngrams
import psycopg2
import pprint
import string
import os

# success is returning:
# West Jerome Avenue
# Country Club Drive
# Baseline Road

pp = pprint.PrettyPrinter(indent=4)

# sentence = open('council_example_text', 'r').readline().translate(string.maketrans("",""), string.punctuation).split()

suffixes = 'Ave Blvd Cir Ct Dr Ln Pl Rd St Way'.split()

prefix = {'North':'N','South':'S','East':'E','West':'W'}
abbr = {'Avenue': 'Ave', 'Boulevard': 'Blvd', 'Circle': 'Cir', 'Court': 'Ct', 'Drive': 'Dr', 'Lane':'Ln', 'Place': 'Pl','Road':'Rd','Street':'St','Way':'Way'}

# TODO - also look for addresses (numbers)
# find and return all roadnames that match test_string in the database.
def find_in_database(test_string):
	# Configuration settings may vary from server to server:
	username = os.environ["DATABASE_URL"].split(":")[1].replace("//","")
	print username
	password = os.environ["DATABASE_URL"].split(":")[2].split("@")[0]
	print password
	host = os.environ["DATABASE_URL"].split(":")[2].split("@")[1].split("/")[0]
	print host
	dbname = os.environ["DATABASE_URL"].split(":")[2].split("@")[1].split("/")[1] 
	print dbname
	conn = psycopg2.connect(dbname=dbname, user=username, password=password, host=host) 

	# print the connection string we will use to connect
	#print "Connecting to database\n	->%s" % (connection_string)

	cursor = conn.cursor()
	#print "Connected!\n"

	# Always use this query: 
	query = "SELECT fullname, ST_ASGeoJSON(geom) FROM mesaroads WHERE fullname ~ '" + test_string + "'"
	cursor.execute(query);

	# retrieve the records from the database
	records = cursor.fetchall()
 
	# print out the records using pretty print
	#print "test string: " + test_string
	cursor.close()
	conn.close()

	return records


# seek_backwards("long ass text here and s alma school rd", 'rd', 8, [])
# seek_backwards("long ass text here and s Alma School rd", 's alma school rd', 5, ['s alma school rd'])


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
def geocode_text(sentence):
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

# cur.execute("SELECT PREDIRABRV as prefix,NAME as name,SUFDIRABRV as suffix, geom FROM featnames LEFT OUTER JOIN roads ON (featnames.TLID = roads.TLID) WHERE name IS NOT NULL;")

# matches = [s for s in cur.fetchall() if (in_twogram(possibilities_2, s[1]) or in_threegram(possibilities_3, s[1])] 
# print "found:"
# print matches
# print sentence

# cur.close()
# conn.close()

# # Given a street name, return the gram(s) that matches (if exists)
# #NEED TO ADD && 
# def in_twogram(grams, name):
# 	return [g for g in grams if g[0] == name]

# def in_threegram(grams, name):
# 	return [g for g in grams if g[1] == name]

# n = 2
# twograms = ngrams(sentence.split(), n)
# possibilities_2 = [x for x in twograms if x[1]=="Street."]
# print possibilities_2

# n = 3
# threegrams = ngrams(sentence.split(), n)
# possibilities_3 = [x for x in threegrams if x[2]=="Street."]
# print possibilities_3

# streets = [['W','8th','St', '123458918292'],['W','68th','St', '8932891982832']]

# conn = psycopg2.connect("dbname=tiger")

# cur = conn.cursor()

# cur.execute("SELECT PREDIRABRV as prefix,NAME as name,SUFDIRABRV as suffix, geom FROM featnames LEFT OUTER JOIN roads ON (featnames.TLID = roads.TLID) WHERE name IS NOT NULL;")

# matches = [s for s in cur.fetchall() if (in_twogram(possibilities_2, s[1]) or in_threegram(possibilities_3, s[1])] 
# print "found:"
# print matches
# print sentence

# cur.close()
# conn.close()


# #searches all the grams for each street name- 
# #if within the gram there is a match for any one word 
# #or two words, then match--grams are limited to those 
# #ending in street, drive, or any other suffix. then limit on prefix. 

# #gram size for road names (road name length in words, and frequency of those)
# #WITH gramsize AS (SELECT name, array_length(regexp_split_to_array(name,'\s'),1) as wordcount FROM featnames) SELECT COUNT(distinct(name)), wordcount from gramsize group by wordcount ORDER BY wordcount DESC;



