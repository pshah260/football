import pandas as pd
import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.espn.com/nfl/stats/player/_/view/defense")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
df = df[0]
df.loc[max(df.index)+1, :] = None
df = df.shift(1, fill_value=df.columns)
df.columns = ["Player"]

soup = BeautifulSoup(res.content,'lxml')
table1 = soup.find_all('table')[1]
df1 = pd.read_html(str(table1))
df1 = df1[0]

df3 = pd.concat([df,df1], axis=1)

print df3
