from flask import Flask, render_template, request, url_for, jsonify
from flask.ext.cors import CORS
from geocoder import *

app = Flask(__name__, static_url_path='')
cors = CORS(app)
app.debug = True

@app.route('/', methods=['GET','POST'])
def index():
	if request.method=='GET':
		return app.send_static_file('index.html')

	if request.method=='POST':
		sentence = request.form['sentence']
		placename = request.form['placename']
		return jsonify(text=geocode_text(sentence,placename))

if __name__ == "__main__":
    app.run()
