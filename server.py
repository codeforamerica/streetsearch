from flask import Flask, render_template, request, url_for, jsonify
from geocoder import *
import string
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--development", help="run with development environment", action="store_true")
args = parser.parse_args()


# Usage:
# To run the server on Heroku: python server.py
# To run the server on your local machine use '-d' for development mode: python server.py -d
# The difference is that on Heroku we pull the database settings out of the DATABASE_URL env variable,
# and on the local machine we expect database to be "tiger" on "localhost" with no authentication required.

if args.development:
	production = False
	environment = "Development"
else:
	production = True
	environment = "Production"


app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def hello():
	global production
	if request.method=='GET':
		return "Hello! See the Makefile for details on testing this. Environment: " + environment

	if request.method=='POST':
		sentence = request.form['fileupload']
		print "Running in Production mode? " + str(production)
		return jsonify(text=geocode_text(production, sentence))

if __name__ == "__main__":
    app.run()