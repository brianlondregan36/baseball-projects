from baseball import app
from flask import render_template, request, redirect, url_for
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/lineupbuilder/')
def builder():
	return render_template("lineupbuilder.html")