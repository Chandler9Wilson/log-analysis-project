SELECT * FROM articles;

SELECT author, slug, title, path FROM articles INNER JOIN log ON articles.slug LIKE log.path;

SELECT title, slug, name FROM articles, authors WHERE articles.author = authors.id;

SELECT title, slug, path
FROM articles, log
WHERE log.path like '%' || articles.slug;

-- This one works pretty well
-- Needs to be improved to filter path better probably using regular expressions
SELECT articles.title, articles.id,
(SELECT COUNT (*)
  FROM log
  WHERE (log.path like '%' || articles.slug AND log.status = '200 OK')) AS requests
FROM articles
ORDER BY requests DESC
LIMIT 3;

-- Works for option 2
SELECT authors.name, 
(SELECT COUNT(*)
  FROM log, articles
  WHERE (log.path like '%' || articles.slug AND log.status = '200 OK')
  AND articles.author = authors.id
) AS requests
FROM authors;


SELECT * FROM log  WHERE status != '200 OK' LIMIT 10;

SELECT articles.title, articles.author,
(SELECT COUNT (*)
  FROM log
  WHERE (log.path like '%' || articles.slug AND log.status = '200 OK')) AS requests
FROM articles
ORDER BY requests DESC;

-- Gets all errors
SELECT DATE(time), COUNT(time) FROM log  WHERE status != '200 OK' GROUP BY CAST(log.time AS DATE) ORDER BY COUNT(time) DESC;

-- Works for option 3
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
WHERE errors_by_day.date = requests_by_day.date AND (errors * 100 / requests) > 1;