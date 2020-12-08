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
    def __init__(self, owner, name, record, pf, pa):
        self.owner=owner
        self.name=name
        self.pf=pf
        self.pa=pa
        self.wins=record[0]
        self.losses=record[1]
        self.ties=record[2]
    
    def __str__(self):
        return self.name

    #set functions
    def setRecord(self, record):
        self.wins=record[0]
        self.losses=record[1]
        self.ties=record[2]

def createTeams(league):#Current Teams and records
    teams = {}

    for team in league.teams:
        teams[team.team_name] = FantasyTeam(team.owner, team.team_name,[team.wins,team.losses,team.ties],team.points_for,team.points_against)
        
    return teams


def chooseWinner(home_team, away_team, override = False): #
    home_ppg = home_team.pf / (home_team.wins + home_team.losses + home_team.ties)
    away_ppg = away_team.pf / (away_team.wins + away_team.losses + away_team.ties)

    home_score = round(random.normal(loc = home_ppg, scale = 18, size=1)[0], 2)
    away_score = round(random.normal(loc = away_ppg, scale = 18, size=1)[0], 2)
    
    home_team.pf+=home_score
    away_team.pf+=away_score

    home_team.pa+=away_score
    away_team.pa+=home_score

    if override:
        if override == 1:
            home_team.wins+=1
            away_team.losses+=1
        elif override == 2:
            home_team.losses+=1
            away_team.wins+=1
        elif override == 3:
            home_team.ties+=1
            away_team.ties+=1
        else:
            raise Exception("InvalidOverride")
    else:
        if home_score > away_score:
            home_team.wins+=1
            away_team.losses+=1
        elif home_score < away_score:
            home_team.losses+=1
            away_team.wins+=1
        else:
            home_team.ties+=1
            away_team.ties+=1


def printLeagueProbabilities(teams, sim_results, iterationsSoFar):
    printf("| %25s | %4s | %4s | %4s | %8s | %8s |\n", "Team Name", "Wins", "Loss", "Ties", "Playoff%","pf")
    printf("------------------------------------------------------------------------\n")
    for owner, team in list(teams.items()):
        printf("| %25s | %4.1f | %4.1f | %4.1f | %8.1f | %8.2f |\n", team.name, sim_results[owner]['wins'], sim_results[owner]['losses'], sim_results[owner]['ties'], sim_results[owner]['appearances'] / float(iterationsSoFar)*100, sim_results[owner]['pf'])
    printf("\n")

def playoffs(teams, sim_results, iterations, slots = 4):
    # teamsSorted does not mutate the param teams
    teamsSorted = sorted(teams.values(), key=operator.attrgetter('wins','ties','losses','pf'), reverse=True)
    for i in range(0, slots):
        sim_results[teamsSorted[i].name]['appearances'] += 1
    for team in teams.values():
        sim_results[team.name]['pf'] += team.pf / iterations
        sim_results[team.name]['wins'] += team.wins / iterations
        sim_results[team.name]['losses'] += team.losses / iterations
        sim_results[team.name]['ties'] += team.ties / iterations

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
        sim_results[team] = {'appearances': 0, 'pf': 0, 'wins': 0, 'losses': 0, 'ties': 0}

    iterations = 100
    printf("Running Sim with %d iterations...\n",iterations)
        
    original_teams = copy.deepcopy(teams)
    for i in range(0, iterations):
        teams = copy.deepcopy(original_teams)
        #simulates week by week
        for week in games_left:
            for home_team, away_team in week:
                chooseWinner(teams[home_team], teams[away_team])
        playoffs(teams, sim_results, iterations)
    printLeagueProbabilities(original_teams, sim_results, iterations)

main()
           
    
