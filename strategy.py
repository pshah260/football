import argparse
from sqlalchemy import create_engine
import pandas as pd

def offence():
    engine = create_engine('postgresql://ai:ai@localhost:5432/football')
    query = "select * from \"OFF\";"
    df = pd.read_sql_query(query,engine)
    return df

def defence():
    engine = create_engine('postgresql://ai:ai@localhost:5432/football')
    query = "select * from \"DEF\";"
    df = pd.read_sql_query(query,engine)
    return df


parser = argparse.ArgumentParser(description='Enter the team names')
parser.add_argument('--away', dest='away', required=True, help='Enter Away Team')
parser.add_argument('--home', dest='home', required=True, help='Enter Home Team')

args = parser.parse_args()

teamA = args.away
teamB = args.home

odf = offence()
ddf = defence()

AOR = odf.Team[odf.Team == teamA].index.tolist()[0] + 1
HOR = odf.Team[odf.Team == teamB].index.tolist()[0] + 1
ADR = ddf.Team[ddf.Team == teamA].index.tolist()[0] + 1
HDR = ddf.Team[ddf.Team == teamB].index.tolist()[0] + 1

print "Away Team offensive ranking", teamA, AOR
print "Home Team offensive ranking", teamB, HOR
print "Away Team defensive ranking", teamA, ADR
print "Home Team defensive ranking", teamB, HDR

A = odf["Team"] == teamA
B = odf["Team"] == teamB
C = ddf["Team"] == teamA
D = ddf["Team"] == teamB

odf = odf[A | B]
ddf = ddf[C | D]


ddf['RYPP'] = ddf['RushingYDS']/ddf['PointsPTS']
ddf['PYPP'] = ddf['PassingYDS']/ddf['PointsPTS']

odf['RYPP'] = odf['RushingYDS']/odf['PointsPTS']
odf['PYPP'] = odf['PassingYDS']/odf['PointsPTS']

ORpointA = odf["RushingYDS/G"][odf.Team == teamA].values[0] / ddf["RYPP"][ddf.Team == teamB].values[0]
OPpointA = odf["PassingYDS/G"][odf.Team == teamA].values[0] / ddf["PYPP"][ddf.Team == teamB].values[0]
ORpointB = odf["RushingYDS/G"][odf.Team == teamB].values[0] / ddf["RYPP"][ddf.Team == teamA].values[0]
OPpointB = odf["PassingYDS/G"][odf.Team == teamB].values[0] / ddf["PYPP"][ddf.Team == teamA].values[0]


DRpointA = ddf["RushingYDS/G"][ddf.Team == teamA].values[0] / odf["RYPP"][odf.Team == teamB].values[0]
DPpointA = ddf["PassingYDS/G"][ddf.Team == teamA].values[0] / odf["PYPP"][odf.Team == teamB].values[0]
DRpointB = ddf["RushingYDS/G"][ddf.Team == teamB].values[0] / odf["RYPP"][odf.Team == teamA].values[0]
DPpointB = ddf["PassingYDS/G"][ddf.Team == teamB].values[0] / odf["PYPP"][odf.Team == teamA].values[0]

AP = round((ORpointA+OPpointA)/2)
BP = round((ORpointB+OPpointB)/2)
CP = round((DRpointA+DPpointA)/2)
DP = round((DRpointB+DPpointB)/2)

ATP = round((AP+DP)/2)
HTP = round((BP+CP)/2)

print "Offense Away Team points: ", teamA, AP, "Breakdown-->", "Rushing:", round(ORpointA/2), "Passing:", round(OPpointA/2)
print "Offense Home Team points: ", teamB, BP, "Breakdown-->", "Rushing:", round(ORpointB/2), "Passing:", round(OPpointB/2)
print "Total Points", AP+BP

print "Defense Away Team points: ", teamA, DP, "Breakdown-->", "Rushing:", round(DRpointB/2), "Passing:", round(DPpointB/2)
print "Defense Home Team points: ", teamB, CP, "Breakdown-->", "Rushing:", round(DRpointA/2), "Passing:", round(DPpointA/2)
print "Total Points", CP+DP

if (ORpointA > OPpointA):
    print "Away team is Rush Heavy --> Go for under"
else:
    print "Away team is Pass Heavy --> Go for over"

if (ORpointB > OPpointB):
    print "Home team is Rush Heavy --> Go for under"
else:
    print "Home team is Pass Heavy --> Go for over"



if AP > BP and DP > CP:
    print "Away Team Wins!"
    if AP >= DP:
        print "Final Away Team points: ", teamA, AP
    else:
        print "Final Away Team points: ", teamA, DP
    if BP <= CP:
        print "Final Home Team points: ", teamB, BP
    else:
        print "Final Home Team points: ", teamB, CP

elif AP < BP and DP < CP:
    print "Home Team Wins!"
    if AP <= DP:
        print "Final Away Team points: ", teamA, AP
    else:
        print "Final Away Team points: ", teamA, DP
    if BP >= CP:
        print "Final Home Team points: ", teamB, BP
    else:
        print "Final Home Team points: ", teamB, CP


else:
    print "Close game! "
    print "Final Away Team points: ", teamA, ATP
    print "Final Home Team points: ", teamB, HTP

