from flask import Flask, render_template, request, url_for, jsonify
from geocoder import *
import string

app = Flask(__name__)
app.debug = True

username = os.environ["DATABASE_URL"].split(":")[1].replace("//","")
password = os.environ["DATABASE_URL"].split(":")[2].split("@")[0]
host = os.environ["DATABASE_URL"].split(":")[2].split("@")[1].split("/")[0]
dbname = os.environ["DATABASE_URL"].split(":")[2].split("@")[1].split("/")[1] 
conn = psycopg2.connect(dbname=dbname, user=username, password=password, host=host) 

@app.route('/', methods=['GET','POST'])
def hello():
	if request.method=='POST':
		sentence = request.form['fileupload']
		#.translate(string.maketrans("",""), string.punctuation).split()
		return jsonify(text=geocode_text(sentence))
	if request.method=='GET':
		return "hello"
if __name__ == "__main__":
    app.run()