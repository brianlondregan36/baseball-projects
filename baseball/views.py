from baseball import app
from flask import render_template, request, redirect, url_for
from teamscores import *

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/lineupbuilder/')
def builder():
	return render_template("lineupbuilder.html")
	


teamCodes = ['TBR', 'NYY', 'TOR', 'BAL', 'BOS', 'KCR', 'MIN', 'DET', 'CLE', 'CHW', 'HOU', 'TEX', 'LAA', 'SEA', 'OAK', 'WSN', 'NYM', 'ATL', 'MIA', 'PHI', 'STL', 'PIT', 'CHC', 'CIN', 'MIL', 'LAD', 'SFG', 'ARI', 'SDP', 'COL']

@app.route('/gauntlet/')
def gauntlet():
	return render_template('gauntlet.html')
	

@app.route('/gauntlet', methods=['GET'])
def rungauntlet():
	year = request.args.get('year', '')
	if year == "":
		return redirect(url_for('index'))
	else:
		teams = {}	
		for i in teamCodes: 
			team = Team(i, year)
			team.FillBuckets() 
			if team.gameNumber != 999:
				teams[team.name] = team.gameNumber
		return render_template('show_results.html', rows=teams)