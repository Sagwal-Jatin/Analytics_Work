-- Define a regular expression pattern to check valid timestamp format
DECLARE TIMESTAMP_REGEX STRING DEFAULT 
r'^\d{4}-\d{1,2}-\d{1,2}[T]\d{1,2}:\d{1,2}:\d{1,2}(\.\d{1,6})? *(([+-]\d{1,2}(:\d{1,2})?)|Z|UTC)?$';

-- Define a regular expression pattern to check valid date format
DECLARE DATA_REGEX STRING DEFAULT
r'^\d(4)-(?:[1-9]|0[1-9]|1[012]-(?:[1-9]\0[1-9]|[12][0-9]\3[01])$';

-- Variables to represent time ranges (can be used later for time-of-day analysis)
DECLARE MORNING_START INT64;
DECLARE MORNING_END INT64;
DECLARE AFTERNOON_END INT64;
DECLARE EVENING_END INT64;

-- Set time boundaries
SET MORNING_START = 6;     -- Morning starts at 6 AM
SET MORNING_END = 12;      -- Morning ends at 12 PM
SET AFTERNOON_END = 18;    -- Afternoon ends at 6 PM
SET EVENING_END = 21;      -- Evening ends at 9 PM;


-- Check how often each column appears across tables
SELECT
  column_name,
  COUNT(table_name) AS table_count
FROM
  `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
GROUP BY
  column_name;


-- Verify which tables contain an ID column
SELECT
  table_name,
  SUM(
    CASE
      WHEN column_name = "id" THEN 1
      ELSE 0
    END
  ) AS has_id_column
FROM
  `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
GROUP BY
  table_name
ORDER BY
  table_name;


-- Find tables that do not contain date or timestamp information
SELECT
  table_name,
  SUM(
    CASE
      WHEN data_type IN ("TIMESTAMP","DATETIME","TIME","DATE")
      THEN 1
      ELSE 0
    END
  ) AS has_time_info
FROM
  `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
WHERE
  data_type IN ("TIMESTAMP","DATETIME","DATE")
GROUP BY
  table_name
HAVING
  has_time_info = 0;


-- List all tables and columns that contain time-related data types
SELECT
  CONCAT(table_catalog,".",table_schema,".",table_name) AS table_path,
  table_name,
  column_name
FROM
  `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
WHERE
  data_type IN ("TIMESTAMP","DATETIME","DATE");


-- Search for columns that are likely related to time or activity tracking
SELECT
  table_name,
  column_name
FROM
  `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
WHERE
  REGEXP_CONTAINS(
    LOWER(column_name),
    "date|minutes|daily|hourly|day|seconds"
  );


-- Check a sample of ActivityDate values to see if they match the timestamp format
SELECT
  ActivityDate,
  REGEXP_CONTAINS(
    STRING(ActivityDate),
    TIMESTAMP_REGEX
  ) AS is_timestamp
FROM
  `bellabeats-492411.daily_activity.daily_activity`
LIMIT 5;


-- Confirm whether all ActivityDate values in the dataset are valid
SELECT
  CASE
    WHEN MIN(
      REGEXP_CONTAINS(
        STRING(ActivityDATE),
        TIMESTAMP_REGEX
      )
    ) = TRUE
    THEN "Valid"
    ELSE "Not Valid"
  END AS valid_test
FROM
  `bellabeats-492411.daily_activity.daily_activity`;


-- Identify tables related to daily-level data
SELECT
  DISTINCT table_name
FROM
  `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
WHERE
  REGEXP_CONTAINS(
    LOWER(table_name),
    "day|daily"
  );


-- Review column types used in daily tables
SELECT
  column_name,
  data_type,
  COUNT(table_name) AS table_count
FROM
  `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
WHERE
  REGEXP_CONTAINS(
    LOWER(table_name),
    "day|daily"
  )
GROUP BY
  column_name,
  data_type;


-- Find columns that appear in multiple daily tables (useful for joins)
SELECT
  column_name,
  table_name,
  data_type
FROM
  `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
WHERE
  REGEXP_CONTAINS(
    LOWER(table_name),
    "day|daily"
  )
  AND column_name IN (
    SELECT
      column_name
    FROM
      `bellabeats-492411.daily_activity.INFORMATION_SCHEMA.COLUMNS`
    WHERE
      REGEXP_CONTAINS(
        LOWER(table_name),
        "day|daily"
      )
    GROUP BY
      column_name
    HAVING
      COUNT(table_name) >= 2
  )
ORDER BY
  column_name;