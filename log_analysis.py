#! /usr/bin/python2.7

import psycopg2

"""
Please create view "article_overview" in database. Execute the following
command:

CREATE VIEW article_overview as
SELECT articles.title, articles.slug,
articles.time article_time, articles.id as article_id,
authors.name as author_name, authors.id as author_id,
log.status, log.time as log_time
FROM articles, authors, log
WHERE articles.author=authors.id
AND articles.slug=replace(log.path, '/article/','')
AND log.path!='/';

\r - This is used for windows pc as \n might not work in windows
"""

DB_NAME = "news"

# Making connection to db
db = psycopg2.connect(dbname=DB_NAME)
c = db.cursor()

print("1. What are the most popular three articles of all time?\r\n")

# Executing queries for question 1
c.execute("SELECT title, count(*) as number "
          "FROM article_overview "
          "GROUP BY title "
          "ORDER BY number DESC limit 3;")
results = c.fetchall()
for r in results:
    print("   %s - %s\r" % r)

print("\r\n\r\n")
print("2. Who are the most popular article authors of all time?\r\n")
c.execute("SELECT author_name, count(*) as article_views "
          "FROM article_overview "
          "GROUP BY author_name "
          "ORDER BY article_views DESC;")
results = c.fetchall()
for r in results:
    print("   %s - %s views\r" % r)

print("\r\n\r\n")
print("3. On which days did more than 1% of requests lead to errors?\r\n")
c.execute("SELECT to_char(t1.my_date1, 'FMMonth DD, YYYY') as my_date, "
          "round((1.0*t2.error_count/t1.total_count)*100, 2) as percentage "
          "FROM (SELECT date(time) as my_date1, count(*) as total_count "
          "FROM log "
          "GROUP BY my_date1 "
          "ORDER BY my_date1) as t1, "
          "(SELECT date(time) as my_date2, count(*) as error_count "
          "FROM log WHERE status!='200 OK' "
          "GROUP BY my_date2 "
          "ORDER BY my_date2) as t2 "
          "WHERE t1.my_date1=t2.my_date2 "
          "AND (1.0*t2.error_count/t1.total_count)*100 > 1;")
results = c.fetchall()
for r in results:
    print("   %s - %s%% errors\r" % r)

print("\r\n\r\n")

# Closing the db connection
db.close()
