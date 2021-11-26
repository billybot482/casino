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
                  white integer,
                  red integer,
                  orange integer,
                  yellow integer,
                  blue integer,
                  purple integer,
                  black integer,
                  wager integer ,
                  worth integer ,
                  win integer ,
                  loss integer,
                  vip integer
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

def add_user(user_id):
  stmt = """INSERT INTO User (user_id, white , red , orange , yellow , blue , purple , black , wager, worth , win , loss , vip)
  VALUES (
  ?,
  100,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  100,
  0,
  0,
  0
)"""
  cur.execute(stmt, (user_id,))
  conn.commit()
  return conn

def get_user_value(user_id: int, items: str):
    stmt = f"SELECT {items} FROM User WHERE user_id=%s;"
    try:
     r= conn.execute(stmt).fetchone()[0]
    except TypeError:
     r = None
    finally:
     return r

def add_white( user_id : int , white : int):
    stmt = f"UPDATE User SET white = white + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_red(user_id : int , white : int):
    stmt = f"UPDATE User SET red = red + %s WHERE user_id %s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_orange(user_id : int , white : int):
    stmt = f"UPDATE User SET orange = orange + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_yellow(user_id : int , white : int):
    stmt = f"UPDATE User SET yellow = yellow + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_blue( user_id : int , white : int):
    stmt = f"UPDATE User SET blue = blue + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_purple(user_id : int , white : int):
    stmt = f"UPDATE User SET purple = purple + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()

def add_black(user_id : int , white : int):
    stmt = f"UPDATE User SET black = black + %s WHERE user_id =%s;"
    cur.execute(stmt, (white,user_id))
    conn.commit()
