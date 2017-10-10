#!/usr/bin/env python
import psycopg2
from tabulate import tabulate

dbInfo = "dbname=news"

def test():
  # Connect to an existing database
  db = psycopg2.connect(dbInfo)
  # Open a cursor to perform database operations
  c = db.cursor()

  c.execute("select author from articles;")
  return c.fetchall()
  db.close()

def interactiveHello():
  intro = raw_input("What's your name? ")
  print("Hello %s lets explore the world!" % intro)

# Return three most popular articles of all time from db
def option1():
  lookFor = '''SELECT title, id,
    (SELECT COUNT (*)
      FROM log
      WHERE (log.path like '%' || articles.slug AND log.status = '200 OK')) AS requests
    FROM articles
    ORDER BY requests DESC
    LIMIT 3;'''
  headers = ["Title", "Author ID", "Article Views"]
  
  # Connect to an existing database
  db = psycopg2.connect(dbInfo)
  # Open a cursor to perform database operations
  c = db.cursor()

  c.execute(lookFor)
  return tabulate(c.fetchall(), headers, tablefmt="psql")
  db.close()

# Return authors sorted by popularity (article views) descending from db
def option2():
  lookFor = '''SELECT authors.name, 
    (SELECT COUNT(*)
      FROM log, articles
      WHERE (log.path like '%' || articles.slug AND log.status = '200 OK')
      AND articles.author = authors.id
    ) AS requests
    FROM authors;'''
  headers = ["Author", "Views"]

  db = psycopg2.connect(dbInfo)
  # Open a cursor to perform database operations
  c = db.cursor()

  c.execute(lookFor)
  return tabulate(c.fetchall(), headers, tablefmt="psql")
  db.close()

# Return days with more than 1% errors
def option3():
  lookFor = '''
    WITH errors_by_day AS (
        SELECT DATE(time), COUNT(time) AS errors
        FROM log
        WHERE status != '200 OK'
        GROUP BY CAST(log.time AS DATE)
      ), requests_by_day AS (
        SELECT DATE(time), COUNT(time) AS requests
        FROM log
        GROUP BY CAST(log.time AS DATE)
      )
    SELECT errors_by_day.date, errors, requests,
    --works but only displays an int
    (errors * 100 / requests) AS percent_errors
    FROM errors_by_day, requests_by_day 
    WHERE errors_by_day.date = requests_by_day.date AND (errors * 100 / requests) > 1;'''
  headers = ["Date", "Errors", "Requests", "Percent Errors"]
  
  db = psycopg2.connect(dbInfo)
  # Open a cursor to perform database operations
  c = db.cursor()

  c.execute(lookFor)
  return tabulate(c.fetchall(), headers, tablefmt="psql")
  db.close()

def interactive():
  # displaying options to the user
  print(30 * '-')
  print('   Report Options')
  print(30 * '-')
  print('1. Three most popular articles of all time')
  print('2. Most popular authors of all time')
  print('3. Days where more than 1% of requests leading to errors')
  print(30 * '-')

  # captures user input
  answer = raw_input('Which report would you like to see: ')
  # catches characters that can't be converted to int
  try:
    answer = int(answer)
  except:
    print(30 * '-')
    print('Invalid option please enter a valid number')
    print(30 * '-')
    return interactive()


  if answer == 1:
    print(30 * '-')
    print('   Results')
    print(30 * '-')
    print(option1())
  elif answer == 2:
    print(30 * '-')
    print('   Results')
    print(30 * '-')
    print(option2())
  elif answer == 3:
    print(30 * '-')
    print('   Results')
    print(30 * '-')
    print(option3())
  else:
    print(30 * '-')
    print('Invalid number try again')
    print(30 * '-')
    return interactive()

interactive()