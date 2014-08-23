from flask import Flask, render_template, request, url_for, jsonify
from geocoder import *
import string
import sys

# Usage:
# To run the server on Heroku: python server.py
# To run the server on your local machine use '-d' for development mode: python server.py -d
# The difference is that on Heroku we pull the database settings out of the DATABASE_URL env variable,
# and on the local machine we expect database to be "tiger" on "localhost" with no authentication required.


if len(sys.argv) == 1:
	production = True
	environment = "Production"
else: # ANY argument passed, assume dev environment.
	production = False
	environment = "Development"


app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def hello():
	global production
	if request.method=='GET':
		return "Hello! See the Makefile for details on testing this. " + environment + ": # args: " + str(len(sys.argv))

	if request.method=='POST':
		sentence = request.form['fileupload']
		print "Running in Production mode? " + str(production)
		return jsonify(text=geocode_text(production, sentence))

if __name__ == "__main__":
    app.run()