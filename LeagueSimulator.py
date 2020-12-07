'''
Created on Feb 1, 2018

@author: Nate
'''
from espn_api.football import League
from numpy import random
import copy
import operator
import sys

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
        self.pa=pa
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

def createTeams(league):#Current Teams and records
    teams = {}

    for team in league.teams:
        teams[team.team_name] = FantasyTeam(team.owner, team.team_name,[team.wins,team.losses,team.ties],team.points_for,team.points_against)
        
    return teams


def chooseWinner(home_team, away_team, override = False): #
    home_ppg = home_team.pf / sum(home_team.record)
    away_ppg = away_team.pf / sum(away_team.record)

    home_score, away_score = random.normal(loc = home_ppg, scale = 18, size=1), random.normal(loc = away_ppg, scale = 18, size=1)
    
    home_team.pf+=home_score
    home_team.pa+=away_score
    away_team.pf+=away_score
    away_team.pa+=home_score

    if override:
        if override == 1:
            home_team.addWin()
            away_team.addLoss()
        elif override == 2:
            home_team.addLoss()
            away_team.addWin()
        else:
            raise Exception("InvalidOverride")
    else:
        if home_score > away_score:
            home_team.addWin()
            away_team.addLoss()
        else:
            home_team.addLoss()
            away_team.addWin()


def printLeagueProbabilities(teams, sim_results, iterationsSoFar):
    printf("| %25s | %4s | %4s | %8s |\n-------------------------------------------\n", "Team Name", "Wins", "Loss", "Playoff%")
    for owner, team in list(teams.items()):
        printf("| %25s | %4d | %4d | %8.1f |\n", team.name , team.getWins(), team.getLosses(), sim_results[owner]['appearances']/float(iterationsSoFar)*100)
    printf("\n")

def playoffs(teams, sim_results, slots = 4):
    # teamsSorted does not mutate the param teams
    teamsSorted = sorted(teams.values(), key=operator.attrgetter('record','pf'), reverse=True)
    for i in range(0, slots):
        sim_results[teamsSorted[i].name]['appearances'] += 1

def main():
    print("Retrieving the Teams from ESPN Fantasy")
    league = League(league_id=1616916, year=2020)
    teams = createTeams(league)
    sim_start_week = 12
    sim_end_week = 13

    print("Retrieving the upcoming matchups from ESPN Fantasy")
    games_left = []
    for i in range(0, sim_end_week - sim_start_week + 1):
        games_left.append([])
        matchups = league.scoreboard(week = sim_start_week + i)
        for matchup in matchups:
            games_left[i].append([matchup.home_team.team_name, matchup.away_team.team_name])
    
    sim_results = {}
    for team in teams.keys():
        sim_results[team] = {'appearances': 0, 'pf': teams[team].pf}

    iterations = 100000
    printf("Running Sim with %d iterations...\n",iterations)
        
    original_teams = copy.deepcopy(teams)
    for i in range(0, iterations):
        teams = copy.deepcopy(original_teams)
        #simulates week by week
        for week in games_left:
            for home_team, away_team in week:
                chooseWinner(teams[home_team], teams[away_team])
        playoffs(teams, sim_results)
    printLeagueProbabilities(original_teams, sim_results, iterations)

main()
           
    
