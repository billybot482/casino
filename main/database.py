
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
                  claimed boolean,
                  slots int
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
                          liquid real,
                          supply real,
                          savedPrice real
                    )
            """)
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS Orders
                    (  
                          user_id int,
                          symbol TEXT,
                          price real,
                          supply real,
                          orderId int
                    )
            """)
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS Pet
                    (
                          type TEXT,
                          user_id int,
                          pet_id int,
                          baby text,
                          teen text,
                          adult text, 
                          growth int, 
                          talent int,
                          distract int,
                          confident int,
                          move1 text,
                          move2 text,
                          move3 text,
                          move4 text,
                          rarity text,
                          special text
                       
                          
                    )
            """)
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS mainpet
                    (
                          type TEXT,
                          user_id int,
                          pet_id int,
                          baby text,
                          teen text,
                          adult text, 
                          growth int, 
                          talent int,
                          distract int,
                          confident int,
                          rarity text,
                          special text
                    )
            """)
    conn.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS PetControl
                    (
                          cat int,
                          dog int,
                          fish int
                    )
            """)
    conn.commit()
    
def add_user(user_id):
  stmt = """INSERT INTO Usr (user_id, white , red , orange , yellow , blue , purple , black , rbwhite , rbred, rborange , rbyellow , rbblue , rbpurple , rbblack, wager , win , loss , vip, rakeback, claimed, slots)
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
  false,
  3
);"""
  cur.execute(stmt, (user_id,))
  conn.commit()
  return conn

def get_cat(user_id):
    stmt = f"SELECT pet_id FROM Pet WHERE type = 'cat' AND user_id = %s;"
    cur.execute(stmt,(user_id,))
    return cur.fetchall()

def get_pet(user_id):
    stmt = f"SELECT pet_id FROM Pet WHERE user_id = %s;"
    cur.execute(stmt,(user_id,))
    return cur.fetchall()

def add_pet_cat(user_id,pet_id , talent , distract , confident):
   stmt = """INSERT INTO Pet (type, user_id ,pet_id , baby , teen , adult , growth , talent , distract , confident , rarity ,special)
  VALUES (
  'cat',
  %s,
  %s,
  'https://telegra.ph/file/f60784ada75e2fe039928.jpg',
  'https://telegra.ph/file/d02fd8f1c2794177a06e7.jpg',
  'https://telegra.ph/file/a60b94e4e180dd3df8055.jpg',
  0,
  %s,
  %s,
  %s,
  'common',
  'pur'
);"""
   cur.execute(stmt, (user_id,pet_id , talent , distract , confident))
   conn.commit()
   return conn 

def pet_control():
  stmt = """INSERT INTO PetControl (cat , dog , fish)
  VALUES (
  20,
  20,
  20
);"""
  cur.execute(stmt)
  conn.commit()
  return conn

def mint_pet(item , amount):
   stmt = f"UPDATE PetControl SET {item} = {item} + %s;"
   cur.execute(stmt, (amount,))
   conn.commit()

def sub_mint(item, amount):
   mint_pet(item, -amount)


def quantity_cat():
    stmt = f"SELECT cat FROM PetControl;"
    cur.execute(stmt)
    return cur.fetchall()
    

def add_stock(name , symbol , liquid, supply):
  stmt = """INSERT INTO Stocks (name , symbol , liquid, supply)
  VALUES (
  %s,
  %s,
  %s,
  %s
);"""
  cur.execute(stmt,(name,symbol,liquid,supply))
  conn.commit()
  return conn

def add_order(name , symbol , price, supply):
  stmt = """INSERT INTO Order (user_id , symbol , price, supply , orderId)
  VALUES (
  %s,
  %s,
  %s,
  %s,
  %s
);"""
  cur.execute(stmt,(user_id ,symbol,price,supply, orderId))
  conn.commit()
  return conn

def pet_control():
  stmt = """INSERT INTO PetControl (cat , dog , fish)
  VALUES (
  20,
  20,
  20
);"""
  cur.execute(stmt)
  conn.commit()
  return conn


def update_price(price , name):
    stmt = "UPDATE Stocks SET price = %s WHERE name = %s;"
    cur.execute(stmt,(price , name))

def reset_daily_claims():
    stmt = "UPDATE Usr SET claimed=false;"
    cur.execute(stmt)
    conn.commit()

def get_stock():
    stmt = f"SELECT name FROM Stocks;"
    cur.execute(stmt)
    return cur.fetchall()

def get_liquid():
    stmt = f"SELECT liquid FROM Stocks;"
    cur.execute(stmt)
    return cur.fetchall()

def get_symbol():
    stmt = f"SELECT symbol FROM Stocks;"
    cur.execute(stmt)
    return cur.fetchall()

def get_supply():
    stmt = f"SELECT supply FROM Stocks;"
    cur.execute(stmt)
    return cur.fetchall()

def get_stock_value(symbol, items):
    stmt = f"SELECT {items} FROM Stocks WHERE symbol =%s;"
    cur.execute(stmt,(symbol,))
    return cur.fetchone()[0] 
    
def get_all_value(items: str):
    stmt = f"SELECT {items} FROM Usr;"
    cur.execute(stmt)
    return cur.fetchall()

def get_user_pet_value(user_id: int,pet_id: int, items: str):
    stmt = f"SELECT {items} FROM Pet WHERE user_id=%s AND WHERE pet_id=%s;"
    cur.execute(stmt, (user_id,pet_id))
    return cur.fetchone()[0]

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


def add_chip(user_id, item, amount):
  stmt = f"UPDATE Usr SET {item} = {item} + %s WHERE user_id = %s;"
  cur.execute(stmt, (amount, user_id))
  conn.commit()

def sub_chip(user_id, item, amount):
  add_chip(user_id, item, -amount)


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
    
def add_slot(user_id : int , vip : int):
    stmt = f"UPDATE Usr SET slots = slots + %s WHERE user_id =%s;"
    cur.execute(stmt, (vip,user_id))
    conn.commit()
    
def add_rbchip(user_id, item, amount):
   stmt = f"UPDATE Usr SET {item} = {item} + %s WHERE user_id = %s;"
   cur.execute(stmt, (amount, user_id))
   conn.commit()

def sub_rbchip(user_id, item, amount):
   add_rbchip(user_id, item, -amount)
 
    
    

def get_average_cash() -> float:
    stmt = "SELECT white, red, orange, yellow, blue, purple, black FROM Usr"
    cur.execute(stmt)
    chips = cur.fetchall()
    stmt = "SELECT COUNT(*) FROM Usr"
    cur.execute(stmt)
    n = cur.fetchone()[0]
    total_worth = sum(map(lambda l: calculate_worth(*l), chips))
    avg_worth = total_worth / n
    return avg_worth

