from flask import Flask, render_template, request, url_for, jsonify
from geocoder import *
import string

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def hello():
	if request.method=='POST':
		# sentence = request.form['fileupload']
		# #.translate(string.maketrans("",""), string.punctuation).split()
		# return jsonify(text=geocode_text(sentence))
	if request.method=='GET':
		return "hello"
if __name__ == "__main__":
    app.run()