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

def interactiveHello():
  intro = raw_input("What's your name? ")
  print("Hello %s lets explore the world!" % intro)

# takes c.fetchall() as the input
# TODO loop to create a generic name for each row then insert into print pattern
def formatTable(input):
  rows = input

  for row in rows:
     # Write rows to text file
     title = str(row[0])
     id = str(row[1])
     results = str(row[2])
     print(title + ' | ' + id + ' | ' + results + '\n')

# Return three most popular articles of all time from db
def option1():
  lookFor = '''SELECT title, id,
    (SELECT COUNT (*)
      FROM log
      WHERE (log.path like '%' || articles.slug AND log.status = '200 OK')) AS requests
    FROM articles
    ORDER BY requests DESC
    LIMIT 3;'''
  # Connect to an existing database
  db = psycopg2.connect(dbInfo)
  # Open a cursor to perform database operations
  c = db.cursor()

  c.execute(lookFor)
  return formatTable(c.fetchall())
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
  db = psycopg2.connect(dbInfo)
  # Open a cursor to perform database operations
  c = db.cursor()

  c.execute(lookFor)
  return c.fetchall()
  db.close()

# Return days with more than 1% errors
def option3():
  

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
    print('3. let me get you those.....')
  else:
    print(30 * '-')
    print('Invalid number try again')
    print(30 * '-')
    return interactive()

interactive()