                             Logs Analysis Project

This program will answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

Assumptions : Database "news" is available and required tables
exists in the database.

How to run this
---------------

- Please create view "article_overview" in database. Execute the following
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

- open command line
- Got to the current folder
- Enter "python log_analysis.py"


Sample Output
---------------

Sample output is saved in output.txt

Libraries
---------------

- psycopg2
