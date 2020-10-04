import pandas as pd
import requests
from bs4 import BeautifulSoup

def abv(team):

    res = requests.get("https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Football_League/National_Football_League_team_abbreviations")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    df = df[0]
    df = df[1:]
    df.columns = ["Abv", "Teams"]

    fteam = df[df["Teams"]==team]["Abv"].values[0]


    return fteam

def fabv(team):

    res = requests.get("https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Football_League/National_Football_League_team_abbreviations")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    df = df[0]
    df = df[1:]
    df.columns = ["Abv", "Teams"]

    fteam = df[df["Abv"]==team]["Teams"].values[0]


    return fteam

