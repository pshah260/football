import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
import time
import requests
from bs4 import BeautifulSoup

def db_table_delete():
    meta_data = "OFF"
    conn_string = "host='localhost' dbname='football' user='ai' password='ai'"
    conn = pg.connect(conn_string)
    cursor = conn.cursor()
    conn.set_isolation_level(0)
    query = "drop table \"" + meta_data + "\";"
    try:
        cursor.execute(query)
    except:
        print("No table to be deleted")

    meta_data = "DEF"
    conn_string = "host='localhost' dbname='football' user='ai' password='ai'"
    conn = pg.connect(conn_string)
    cursor = conn.cursor()
    conn.set_isolation_level(0)
    query = "drop table \"" + meta_data + "\";"
    try:
        cursor.execute(query)
    except:
        print("No table to be deleted")


def db_push():
    engine = create_engine('postgresql://ai:ai@localhost:5432/football')
    df = offence()
    df.columns = df.columns.map(''.join)
    df.to_sql("OFF",engine)
    df = defence()
    df.columns = df.columns.map(''.join)
    df.to_sql("DEF",engine)


def offence():
    res = requests.get("https://www.espn.com/nfl/stats/team/_/table/passing/sort/netYardsPerGame/dir/desc")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    df = df[0]
    df.loc[max(df.index)+1, :] = None
    df = df.shift(1, fill_value=df.columns)
    df.columns = ["Team"]
    table1 = soup.find_all('table')[1]
    df1 = pd.read_html(str(table1))
    df1 = df1[0]
    df3 = pd.concat([df,df1], axis=1)
    return df3

def defence():
    res = requests.get("https://www.espn.com/nfl/stats/team/_/view/defense/table/passing/sort/netYardsPerGame/dir/asc")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    df = df[0]
    df.loc[max(df.index)+1, :] = None
    df = df.shift(1, fill_value=df.columns)
    df.columns = ["Team"]
    table1 = soup.find_all('table')[1]
    df1 = pd.read_html(str(table1))
    df1 = df1[0]
    df3 = pd.concat([df,df1], axis=1)
    return df3

if __name__ == "__main__":
    db_table_delete()
    db_push()
