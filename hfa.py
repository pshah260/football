import pandas as pd
import requests
from bs4 import BeautifulSoup

def hfa(team):

    res = requests.get("https://www.cbssports.com/nfl/news/nfl-betting-tips-how-much-home-field-advantage-is-worth-for-every-nfl-team-in-2019/")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    df = df[0]

    fteam = df[df["Team"]==team]["2019"].values[0]

    return fteam
