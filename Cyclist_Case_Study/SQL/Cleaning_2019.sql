-- Select specific columns from the 2019 dataset
SELECT 
  trip_id,        -- Unique identifier for each trip
  usertype,       -- Type of rider (Subscriber or Customer)
  start_time,     -- Timestamp when the trip started
  end_time,       -- Timestamp when the trip ended

  -- Create a new column called ride_length formatted as HH:MM:SS
  FORMAT('%02d:%02d:%02d',

    -- Calculate hours:
    -- Get total trip duration in seconds and divide by 3600 to convert to hours
    DIV(TIMESTAMP_DIFF(end_time, start_time, SECOND), 3600),

    -- Calculate minutes:
    -- Convert total seconds to minutes, then use MOD to get remaining minutes after hours
    MOD(
        DIV(TIMESTAMP_DIFF(end_time, start_time, SECOND), 60),
        60
    ),

    -- Calculate seconds:
    -- Get the remaining seconds after minutes are calculated
    MOD(
        TIMESTAMP_DIFF(end_time, start_time, SECOND),
        60
    )

  ) AS ride_length,   -- Name of the calculated column showing ride duration

  -- Create a new column showing the day of the week (e.g., Monday, Tuesday)
  FORMAT_DATE('%A', DATE(start_time)) AS day_of_week

-- Specify the dataset and table to retrieve data from
FROM `cyclisticcasestudy-482512.cycleuseradata.2019`

-- Filter out invalid trips
-- This keeps only trips where the end time is after the start time
WHERE
  TIMESTAMP_DIFF(end_time, start_time, SECOND) > 0