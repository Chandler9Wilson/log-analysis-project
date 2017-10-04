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

SELECT SUM(requests) from (
  SELECT COUNT(*)
  FROM log, articles
  WHERE (log.path like '%' || articles.slug AND log.status = '200 OK')
) AS requests;


SELECT * FROM log  WHERE status != '200 OK' LIMIT 10;