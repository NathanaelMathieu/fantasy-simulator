'''
Created on Feb 1, 2018

@author: Nate
'''
import random
import sys
import operator

def printf(format1, *args):
    sys.stdout.write(format1 % args)

playoffAppearances=[0]

class IntramuralTeam(object):
    '''
    classdocs
    '''
    numberOfTeams=0
    def __init__(self,number,teamName,record):
        self.number=number
        self.teamName=teamName
        if len(record) == 3:
            self.record = record
        else:
            self.record=[record[0],record[1],0]
    
    #get functions
    def getNumber(self):
        return self.number
    def getName(self):
        return self.teamName
    def getRecord(self):
        return self.record
    def getWins(self):
        return self.record[0]
    def getLosses(self):
        return self.record[1]
    def getTies(self):
        return self.record[2]

  
    
    #set functions
    def setRecord(self,record):
        for i in range(0, 3):
            self.record[i] = record[i]
    def addWin(self):
        self.record[0]+=1
    def addLoss(self):
        self.record[1]+=1
        
def createTeams():#Current Teams and records
    teams = {} # teams should be a dictionary
    teams["Adam"] = IntramuralTeam (1,"Team Linsky",[8,3])
    teams["Jonathan"] = IntramuralTeam (2,"IM NOT PAYING",[8,3])
    teams["Andrew"] = IntramuralTeam (3,"Sea Monsters",[8,3])
    teams["Jack"] = IntramuralTeam (4,"Free Elf",[7,4])
    teams["Nate"] = IntramuralTeam (5,"Trust The Process",[7,4])
    teams["Jake"] = IntramuralTeam (6,"Team Momo",[7,4])
    teams["Bailey"] = IntramuralTeam (7,"Tryin My Best",[7,4])
    teams["Eric"] = IntramuralTeam (8,"Cleveland Busters",[4,7])
    teams["Geoff"] = IntramuralTeam (9,"The Fox Den",[3,8])
    teams["Henry"] = IntramuralTeam (10,"Champs",[3,8])
    teams["Sherman"] = IntramuralTeam (11,"Team Mak",[2,9])
    teams["George"] = IntramuralTeam (12,"Team Sheepie",[2,9])

    for i in range(0,len(teams)-1):
        playoffAppearances.append(0)
        
    return teams
    
def chooseWinner(team1,team2,probability):#each team wins 50% of the time  
    if(random.uniform(0,1)<probability):
        team1.addWin()
        team2.addLoss()
    else:
        team1.addLoss()
        team2.addWin()

def sort(teams):#nonfunctional and replaced by line 103 (after the commented out call to this fxn)
    newTeams=teams
    for i in range(0,len(teams)):
        for j in range(i,0):
            if newTeams[j].getWins() > newTeams[j-1].getWins():
                swap=newTeams[j]
                newTeams[j]=newTeams[j-1]
                newTeams[j-1]=swap
            else:
                break
    return newTeams
def printLeagueProbabilities(intramuralC,iterationsSoFar):
    printf("| %15s | %4s | %4s | %8s |\n-------------------------------------------\n", "Team Name", "Wins", "Loss", "Playoff%")
    for n in range(0,8):
        printf("| %15s | %4d | %4d | %8.1f |\n", intramuralC[n].getName() , intramuralC[n].getWins(), intramuralC[n].getLosses(), playoffAppearances[intramuralC[n].getNumber()-1]/float(iterationsSoFar)*100)
    printf("\n\n")


def playoffs(teams):
    playoffSlots=6
    playoffTeams=0
    tiebreakerCount=0
    i=0
    while playoffTeams < playoffSlots:
        if teams[i].getWins() > teams[i+1].getWins():
            if tiebreakerCount==0:
                playoffAppearances[teams[i].getNumber()-1]+=1
                playoffTeams+=1
            elif tiebreakerCount + playoffTeams <= playoffSlots:
                for n in range(0,tiebreakerCount+1):
                    playoffAppearances[teams[i-n].getNumber()-1]+=1
                    playoffTeams+=1
                tiebreakerCount=0
            else:
                slotsLeft=playoffSlots-playoffTeams
                selected=random.sample(range(0,tiebreakerCount+1),slotsLeft)
                for n in range(0, len(selected) ):
                    playoffAppearances[teams[i-selected[n]].getNumber()-1] += 1
                    playoffTeams+=1
                tiebreakerCount=0
            i+=1
        else:
            i+=1
            tiebreakerCount+=1                  
def main():
    half=.5
    gamesLeft = []

    iterations = 100000
    printf("\nRunning Sim with %d iterations...\n",iterations)
    
    for i in range(0,iterations):
        intramuralC = createTeams()
        #simulates week by week
        for k in range(0,len(gamesLeft)):
            for j in range(0,len(gamesLeft[k])):
                chooseWinner(intramuralC[gamesLeft[k][j][0]], intramuralC[gamesLeft[k][j][1]], gamesLeft[k][j][2])

        intramuralCSorted = sorted(intramuralC.values(), key=operator.attrgetter('record'), reverse=True)
        playoffs(intramuralCSorted)
        printLeagueProbabilities(intramuralCSorted, i+1)
main()
           
    
