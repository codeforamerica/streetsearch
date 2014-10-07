from flask import Flask, render_template, request, url_for, jsonify
from flask.ext.cors import CORS
from geocoder import *

app = Flask(__name__, static_url_path='')
cors = CORS(app)
app.debug = True

@app.route('/', methods=['GET','POST'])
def hello():
	if request.method=='GET':
		return app.send_static_file('index.html')

	if request.method=='POST':
		sentence = request.form['fileupload']
		return jsonify(text=geocode_text(sentence))

if __name__ == "__main__":
    app.run()
