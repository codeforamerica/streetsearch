from flask import Flask, render_template, request, url_for, jsonify
from geocoder import *

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def hello():
	if request.method=='GET':
		return "Hello! See the Makefile for details on testing this."

	if request.method=='POST':
		sentence = request.form['fileupload']
		return jsonify(text=geocode_text(sentence))

if __name__ == "__main__":
    app.run()