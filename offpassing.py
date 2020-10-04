import pandas as pd
import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.espn.com/nfl/stats/player")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
df = df[0]

soup = BeautifulSoup(res.content,'lxml')
table1 = soup.find_all('table')[1]
df1 = pd.read_html(str(table1))
df1 = df1[0]

df3 = pd.concat([df,df1], axis=1)

print df3
