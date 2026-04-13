SELECT *
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
LIMIT 10;

SELECT COUNT(*)
FROM `amazonbooks-493111.amazon_books_db.amazon_books`;

SELECT
  MAX(price),
  MIN(price),
  MIN(`User Rating`) AS user_rating,
  MAX(`User Rating`) AS max_user_rating
FROM
  `amazonbooks-493111.amazon_books_db.amazon_books`;


CREATE OR REPLACE TABLE `amazonbooks-493111.amazon_books_db.amazon_books` AS
SELECT * EXCEPT(row_num)
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY Name, Author, Year ORDER BY Price ASC) as row_num
  FROM `amazonbooks-493111.amazon_books_db.amazon_books`
)
WHERE row_num = 1;

SELECT *
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
WHERE
  Name IS NULL
  OR Author IS NULL
  OR Price IS NULL;

UPDATE `amazonbooks-493111.amazon_books_db.amazon_books`
SET Genre = TRIM(Genre)
WHERE TRUE;

SELECT*
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
WHERE Price < 0;

ALTER TABLE `amazonbooks-493111.amazon_books_db.amazon_books`
ADD COLUMN IF NOT EXISTS rating_category STRING;

UPDATE `amazonbooks-493111.amazon_books_db.amazon_books`
SET rating_category =
CASE
  WHEN `User Rating` >= 4.5 THEN 'Excellent'
  ELSE 'Average'
END
WHERE TRUE;

ALTER TABLE `amazonbooks-493111.amazon_books_db.amazon_books`
ADD COLUMN IF NOT EXISTS price_category STRING;

UPDATE `amazonbooks-493111.amazon_books_db.amazon_books`
SET price_category =
CASE
  WHEN Price >= 15 THEN 'Expensive'
  ELSE 'Affordable'
END
WHERE TRUE;

SELECT
  Genre,
  COUNT(*) AS total_books
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
GROUP BY Genre
ORDER BY total_books DESC;

SELECT
  Genre,
  ROUND(AVG(`User Rating`), 2) AS avg_rating
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
GROUP BY Genre;

SELECT
  Genre,
  ROUND(AVG(Price),2) AS average_price
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
GROUP BY Genre;

SELECT
  Author,
  COUNT(*) AS total_books
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
GROUP BY Author
ORDER BY total_books DESC
LIMIT 10;

SELECT
  Year,
  ROUND(AVG(Reviews), 2) AS average_reviews
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
GROUP BY Year
ORDER BY average_reviews DESC;

SELECT
  Name,
  Reviews
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
ORDER BY Reviews DESC
LIMIT 10;

CREATE TABLE IF NOT EXISTS `amazonbooks-493111.amazon_books_db.genre_summary` AS
SELECT
  Genre,
  COUNT(*) AS total_books,
  AVG(`User Rating`) AS avg_rating,
  AVG(Price) AS average_price
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
GROUP BY Genre;

SELECT *
FROM`amazonbooks-493111.amazon_books_db.amazon_books`
WHERE Genre = 'Fiction';

SELECT *
FROM`amazonbooks-493111.amazon_books_db.amazon_books`
ORDER BY Price DESC
LIMIT 10;

SELECT
  Genre,
  COUNT(*)
FROM `amazonbooks-493111.amazon_books_db.amazon_books`
GROUP BY Genre;

SELECT
  Name,
  CASE
      WHEN Price > 20 THEN 'High'
      ELSE 'Low'
  END AS price_level
FROM`amazonbooks-493111.amazon_books_db.amazon_books`;

SELECT *
FROM `amazonbooks-493111.amazon_books_db.amazon_books`;