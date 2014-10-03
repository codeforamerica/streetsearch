import psycopg2
import string
import os
import logging
from pygeocoder import Geocoder
from geojson import Point

# success is returning:
# West Jerome Avenue
# Country Club Drive
# Baseline Road

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

suffixes = 'Ave Blvd Cir Ct Dr Ln Pl Rd St Way'.split()

prefix = {'North':'N','South':'S','East':'E','West':'W'}
abbr = {'Avenue': 'Ave', 'Boulevard': 'Blvd', 'Circle': 'Cir', 'Court': 'Ct', 'Drive': 'Dr', 'Lane':'Ln', 'Place': 'Pl','Road':'Rd','Street':'St','Way':'Way'}

# find and return all roadnames that match test_string in the database.
# test_string: something that might be a street name (or part of one)
def find_in_database(test_string):

	if 'DATABASE_URL' in os.environ:
		# Configuration settings may vary from server to server:
		# db_url = os.environ["DATABASE_URL"]
		logger.info(os.environ["DATABASE_URL"])
		username = os.environ["DATABASE_URL"].split(":")[1].replace("//","")
		password = os.environ["DATABASE_URL"].split(":")[2].split("@")[0]
		host = os.environ["DATABASE_URL"].split(":")[2].split("@")[1].split("/")[0]
		dbname = os.environ["DATABASE_URL"].split(":")[3].split("/")[1]
		dbport = os.environ["DATABASE_URL"].split(":")[3].split("/")[0]
		logger.info("database name: " + dbname)
		db_conn = psycopg2.connect(dbname=dbname, user=username, password=password, host=host,port=dbport)
	else:
		db_conn = psycopg2.connect(dbname='tiger', host='localhost', port='5432')


	cursor = db_conn.cursor()
	logger.debug("Connected to database.\n")

	queryd = "SELECT * FROM mesaroads limit 1;"
	cursor.execute(queryd)
	records = cursor.fetchall()
	logger.debug(records)

	# Always use this query:
	query = "SELECT fullname, ST_ASGeoJSON(geom) FROM mesaroads WHERE fullname ~ '" + test_string + "'"
	cursor.execute(query);

	# retrieve the records from the database
	records = cursor.fetchall()
	cursor.close()
	db_conn.close()

	return records


def is_number(num_or_not):
	try:
	    int(num_or_not)
	except ValueError:
	    return False
	else:
	    return True

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
	logger.debug('text | fragment | index | matches %s | %s | %s | %s' % (text,fragment,index,matches))
	if index == 0:
		return matches
	prev_index = index - 1

	this_word = text[prev_index]
	logger.debug(this_word)
	if this_word in prefix.keys():
		this_word = prefix[this_word]

	test_string = this_word + ' ' + fragment
	logger.debug(test_string)
	# get locations = matches for p + suffix in roads database/name column
	new_matches = find_in_database(test_string)
	logger.debug("testing %s resulted in new matches:" % test_string)
	logger.debug(new_matches)
	if len(new_matches) == 0:
		logger.debug("no new matches based on '%s', returning former matches" % this_word)
		return matches # stick w/ old results
	elif len(new_matches) == 1:
		if prev_index > 0: # start looking for address to geocode
			maybe_address_number = text[prev_index-1]
			if is_number(maybe_address_number):
				maybe_address = maybe_address_number + ' ' + test_string
				logger.debug('Address to Geocode (TODO): %s' % maybe_address)
				results = Geocoder.geocode(maybe_address + ' Mesa, AZ')
				logger.debug('Geocoder returned this location:')
				logger.debug(results[0].coordinates)

				if len(results) > 0:
					geocoded_match = (maybe_address, '%s' % Point(results[0].coordinates))
					logger.debug(geocoded_match)
					logger.debug("Found specific geocoded match; returning it")
					return [geocoded_match]

		logger.debug("down to 1 line match for '%s', returning match\n\n" % test_string)

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

	if 'DEBUG' in os.environ:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)

	sentence = sentence.encode('utf8')
	sentence = sentence.translate(string.maketrans("",""), string.punctuation).split() #strip punctuation

	all_matches = []
	for i, word in enumerate(sentence):
		if word in abbr.keys(): # Abbrieviate all road types (e.g. Road -> Rd) to match our little list of suffixes
			word = abbr[word]
		if word in suffixes:
			logger.info("seeking backwards from " + word + " at index: " + str(i))
			these_matches = seek_backwards(sentence, word, i, [])
			logger.info(these_matches)
			if these_matches:
				all_matches += these_matches

	logger.info(all_matches)
	return all_matches
