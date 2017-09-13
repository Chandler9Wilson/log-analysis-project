#!/usr/bin/env python
import psycopg2

dbInfo = "dbname=news"

def test():
  # Connect to an existing database
  db = psycopg2.connect(dbInfo)
  # Open a cursor to perform database operations
  c = db.cursor()

  c.execute("select author from articles;")
  return c.fetchall()
  db.close()

def interactive():
  intro = raw_input("What's your name? ")
  print("Hello %s lets explore the world!" % intro)

interactive()