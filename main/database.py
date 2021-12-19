
from main.cash import calculate_worth
from typing import *
import os
import psycopg2


def init(url):
    global conn, cur
    conn = psycopg2.connect(url, sslmode='require')
    cur = conn.cursor()
    print(url)

def setup():
    conn.autocommit = True
    cur.execute("SELECT VERSION();")
    print("Connected to", cur.fetchone())
    cur.execute("""CREATE TABLE IF NOT EXISTS Usr
            (
                 user_id int not null primary key,
                  white real,
                  red real,
                  orange real,
                  yellow real,
                  blue real,
                  purple real,
                  black real,
                  rbwhite real,
                  rbred real,
                  rborange real,
                  rbyellow real,
                  rbblue real,
                  rbpurple real,
                  rbblack real,
                  wager real ,
                  win integer ,
                  loss integer,
                  vip integer,
                  rakeback real,
                  claimed boolean
            );
    """)
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS title
                    (
                          title text

                    )
            """)
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS Club
                    (
                          club1 TEXT,
                          club2 TEXT,
                          club3 TEXT,
                          club4 TEXT

                    )
            """)
    conn.commit()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Stocks
                    (
                          name TEXT,
                          symbol TEXT,
                          price UNSIGNED INT,
                          supply UNSIGNED INT

                    )
            """)
    conn.commit()

def add_user(user_id):
  stmt = """INSERT INTO Usr (user_id, white , red , orange , yellow , blue , purple , black , rbwhite , rbred, rborange , rbyellow , rbblue , rbpurple , rbblack, wager , win , loss , vip, rakeback, claimed)
  VALUES (
  %s,
  100,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  false
);"""
  cur.execute(stmt, (user_id,))
  conn.commit()
  return conn

def reset_daily_claims():
    stmt = "UPDATE Usr SET claimed=false;"
    cur.execute(stmt)
    conn.commit()

def add_stock(name , symbol , price, supply):
    stmt = "UPDATE Stocks SET price = %s WHERE name = %name;"
    cur.execute(stmt,(name , symbol ,price , supply))
    conn.commit()
    
def get_stock(name):
    stmt = f"SELECT {name} FROM Stocks;"
    cur.execute(stmt)
    return cur.fetchall()
    
    
def get_user_value(user_id: int, items: str):
    stmt = f"SELECT {items} FROM Usr WHERE user_id=%s;"
    cur.execute(stmt, (user_id,))
    return cur.fetchone()[0]

def set_user_value(user_id: int, item: str, value: Any):
    stmt = f"""UPDATE Usr
                SET {item} = %s
                WHERE user_id = %s"""
    cur.execute(stmt, (value, user_id))
    conn.commit()


def add_white( user_id : int , white : int):
    stmt = f"UPDATE Usr SET white = white + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_red(user_id : int , white : int):
    stmt = f"UPDATE Usr SET red = red + %s WHERE user_id = %s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_orange(user_id : int , white : int):
    stmt = f"UPDATE Usr SET orange = orange + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_yellow(user_id : int , white : int):
    stmt = f"UPDATE Usr SET yellow = yellow + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_blue( user_id : int , white : int):
    stmt = f"UPDATE Usr SET blue = blue + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_purple(user_id : int , white : int):
    stmt = f"UPDATE Usr SET purple = purple + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_black(user_id : int , white : int):
    stmt = f"UPDATE Usr SET black = black + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()
    
def add_wager(user_id : int , white : int):
    stmt = f"UPDATE Usr SET wager = wager + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()
    
def add_win(user_id : int , white : int):
    stmt = f"UPDATE Usr SET win = win + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()
    
def add_loss(user_id : int , white : int):
    stmt = f"UPDATE Usr SET loss = loss + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_vip(user_id : int , vip : int):
    stmt = f"UPDATE Usr SET vip = vip + %s WHERE user_id =%s;"
    cur.execute(stmt, (vip,user_id))
    conn.commit()
    
def add_rbwhite( user_id : int , white : int):
    stmt = f"UPDATE Usr SET rbwhite = rbwhite + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()    
    
def add_rbred( user_id : int , white : int):
    stmt = f"UPDATE Usr SET rbred = rbred + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()    
     
def add_rborange( user_id : int , white : int):
    stmt = f"UPDATE Usr SET rborange = rborange + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()    
    
def add_rbyellow( user_id : int , white : int):
    stmt = f"UPDATE Usr SET rbyellow = rbyellow + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()  
    
def add_rbblue( user_id : int , white : int):
    stmt = f"UPDATE Usr SET rbblue = rbblue + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()  
    
def add_rbpurple( user_id : int , white : int):
    stmt = f"UPDATE Usr SET rbpurple = rbpurple + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()  
    
def add_rbblack( user_id : int , white : int):
    stmt = f"UPDATE Usr SET rbblack = rbblack + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def get_average_cash() -> float:
    stmt = "SELECT white, red, orange, yellow, blue, purple, black FROM Usr"
    cur.execute(stmt)
    chips = cur.fetchall()
    stmt = "SELECT COUNT(*) FROM Usr"
    cur.execute(stmt)
    n = cur.fetchone()
    total_worth = sum(map(lambda l: calculate_worth(*l), chips))
    avg_worth = total_worth / n
    return avg_worth

