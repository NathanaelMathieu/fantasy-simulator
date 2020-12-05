'''
Created on Feb 1, 2018

@author: Nate
'''
import random
import sys
import operator

def printf(format1, *args):
    sys.stdout.write(format1 % args)

class FantasyTeam(object):
    '''
    classdocs
    '''
    def __init__(self,owner,name,record,pf,pa):
        self.owner=owner
        self.name=name
        self.pf=pf
        self.pf=pa
        if len(record) == 3:
            self.record = record
        else:
            self.record=[record[0],record[1],0]
    
    def __str__(self):
        return self.name
    
    #get functions
    def getWins(self):
        return self.record[0]
    def getLosses(self):
        return self.record[1]
    def getTies(self):
        return self.record[2]

    #set functions
    def setRecord(self,record):
        for i in range(0, min(3, len(record))):
            self.record[i] = record[i]
    def addWin(self):
        self.record[0]+=1
    def addLoss(self):
        self.record[1]+=1
        
def createTeams():#Current Teams and records
    teams = {}
    teams["Adam"] = FantasyTeam ("Adam","Team Linsky",[9,3])
    teams["Jonathan"] = FantasyTeam ("Jonathan","IM NOT PAYING",[9,3])
    teams["Andrew"] = FantasyTeam ("Andrew","Sea Monsters",[9,3])
    teams["Jack"] = FantasyTeam ("Jack","Free Elf",[7, 5])
    teams["Nate"] = FantasyTeam ("Nate","Trust The Process",[7,5])
    teams["Jake"] = FantasyTeam ("Jake","Team Momo",[8,4])
    teams["Bailey"] = FantasyTeam ("Bailey","Tryin My Best",[7,5])
    teams["Eric"] = FantasyTeam ("Eric","Cleveland Busters",[4,8])
    teams["Geoff"] = FantasyTeam ("Geoff","The Fox Den",[4,8])
    teams["Henry"] = FantasyTeam ("Henry","Champs",[4,8])
    teams["Sherman"] = FantasyTeam ("Sherman","Team Mak",[2,10])
    teams["George"] = FantasyTeam ("George","Team Sheepie",[2,10])
        
    return teams
    
def chooseWinner(team1,team2,probability):#each team wins 50% of the time  
    if(random.uniform(0, 1)<probability):
        team1.addWin()
        team2.addLoss()
    else:
        team1.addLoss()
        team2.addWin()

def printLeagueProbabilities(teams, playoffAppearances, iterationsSoFar):
    printf("| %20s | %4s | %4s | %8s |\n-------------------------------------------\n", "Team Name", "Wins", "Loss", "Playoff%")
    for owner, team in list(teams.items()):
        printf("| %20s | %4d | %4d | %8.1f |\n", team.getName() , team.getWins(), team.getLosses(), playoffAppearances[owner]/float(iterationsSoFar)*100)
    printf("\n\n")

def playoffs(teams, playoffAppearances, slots = 4):
    # teamsSorted does not mutate the param teams
    teamsSorted = sorted(teams.values(), key=operator.attrgetter('record'), reverse=True)
    for i in range(0, slots):
        playoffAppearances[teamsSorted[i].getOwner()] += 1

def main():
    gamesLeft = [[["Nate","Geoff",0.5],["George","Sherman",0.5],["Eric","Henry",0.5],["Andrew","Jonathan",0.5],["Adam","Jake",0.5],["Bailey","Jack",0.5]]]
    
    playoffAppearances = {}
    for team in createTeams().keys():
        playoffAppearances[team] = 0

    iterations = 10000
    printf("\nRunning Sim with %d iterations...\n",iterations)
    
    
    for i in range(0, iterations):
        teams = createTeams()
        #simulates week by week
        for week in gamesLeft:
            for game in week:
                chooseWinner(teams[game[0]], teams[game[1]], game[2])
        playoffs(teams, playoffAppearances, 6)
    printLeagueProbabilities(teams, playoffAppearances, iterations)

main()
           
    
