import urllib2
from BeautifulSoup import BeautifulSoup

class Team(object):
    
    def __init__(self, name, year):
        '''
        INPUT: a team code or name
        url = a link to the team's data on baseball-reference.com
        games = list containing all of the game numbers, typically 1 through 162
        gameNumber = the point in the season when the has team scored every run total 
        runBuckets = the games where 1 run was scored, games where 2 runs were scored, up through 13
        '''       
        self.name = name
        self.year = str(year)
        self.url = "http://www.baseball-reference.com/teams/" + self.name + "/" + self.year + "-schedule-scores.shtml"   
        self.games = []      
        self.gameNumber = 999
        self.runBuckets = []
        for i in range(0,13):  
            self.runBuckets.append([])
                
    def FillBuckets(self):
        print "\n "+ self.name + " - loading team's scores from baseball-reference.com"
        page = urllib2.urlopen(self.url)
        soup = BeautifulSoup(page.read())

        top = soup.find("table", {"id": "team_schedule"}).tbody
        for thisRow in top.findAll('tr'):  #go through each row
            if "preview" in thisRow.text:
                #season still in progress, reached a game that hasn't been played yet
                break
            else: 
                cellIndex = 1
                for thisCell in thisRow.findAll('td'):  #go through each cell 
                    if cellIndex == 1:
                        if (thisCell.string == "Rk") or (thisCell is None) or (len(thisCell) == 0):  
                            #skip the occassional header row
							break
                    if cellIndex == 2:  
                        #add this game number to the team's games list
                        self.games.append(thisCell.string)
                    if cellIndex == 9:   
                        #get this game's runs scored
						score = int(thisCell.string)
						if score >= 1 and score <= 13:
							#add this game number to the run bucket it belongs in
							self.runBuckets[score-1].append(len(self.games))
                    cellIndex += 1
                #after you grab a game, check if the team closed out all the run buckets
                self.EveryRunBucket()
        
    def EveryRunBucket(self):
        if self.gameNumber == 999:  #the team didn't do it yet
            update = True
            for i in self.runBuckets:
                if len(i) == 0:  
                    #if any of the run buckets are empty, the team didn't do it yet
					update = False
					break
            if update == True:   #none of the run buckets were empty...
                #the team has scored at least once, every run total we're interested in
                #set the gameNumber they could finally say this at
				self.gameNumber = len(self.games)
                                       
    def GetTeamCounts(self):
        '''
        OUTPUT: a list containing the number of games a team scored x number of runs
        '''
        vals = []
        for i in range(len(self.runBuckets)): 
            count = len(self.runBuckets[i])
            vals.append(count)
        return vals