from baseball import app
from teamscores import *
from flask import Flask, render_template, request, redirect, url_for
import Queue
import threading

teamCodes = ['TBR', 'NYY', 'TOR', 'BAL', 'BOS', 'KCR', 'MIN', 'DET', 'CLE', 'CHW', 'HOU', 'TEX', 'LAA', 'SEA', 'OAK', 'WSN', 'NYM', 'ATL', 'MIA', 'PHI', 'STL', 'PIT', 'CHC', 'CIN', 'MIL', 'LAD', 'SFG', 'ARI', 'SDP', 'COL']
queue = Queue.Queue()
teams = {}

class ThreadUrl(threading.Thread):
    def __init__(self, queue, year):
        threading.Thread.__init__(self)
        self.queue = queue
        self.year = year
        
    def run(self):
        while True:
            teamCode = self.queue.get()
            team = Team(teamCode, year)
            team.FillBuckets()
            if team.gameNumber != 999:
                teams[team.name] = team.gameNumber
            self.queue.task_done()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/lineupbuilder/')
def builder():
    return render_template("lineupbuilder.html")
    
@app.route('/runsscoredgauntlet/')
def gauntletpage():
    return render_template("runsscoredgauntlet.html")

@app.route('/gauntlet', methods=['GET'])
def runGauntlet():
    print "hi there"
    year = request.args.get('year', '')
    if year == "":
        return redirect(url_for('index'))
    else:
        for i in range(5):
            t = ThreadUrl(queue, year)
            t.setDaemon(True)
            t.start()
        for teamCode in teamCodes:
            queue.put(teamCode)
            print "\n " + "the length of the queue is " + queue.len
        queue.join()
        print "\n " + "k done now"
        return render_template('show_results.html', rows=teams)