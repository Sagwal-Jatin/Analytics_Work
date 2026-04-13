-- Select specific columns from the dataset
SELECT 
  ride_id,            -- Unique identifier for each bike ride
  started_at,         -- Timestamp when the ride started
  ended_at,           -- Timestamp when the ride ended
  member_casual,      -- Indicates whether the rider is a member or casual user

  -- Create a new column called ride_length formatted as HH:MM:SS
  FORMAT('%02d:%02d:%02d',

    -- Calculate hours:
    -- Get total ride duration in seconds, then divide by 3600 to convert to hours
    DIV(TIMESTAMP_DIFF(ended_at, started_at, SECOND), 3600),

    -- Calculate minutes:
    -- First convert total seconds to minutes, then use MOD to get remaining minutes after hours
    MOD(
        DIV(TIMESTAMP_DIFF(ended_at, started_at, SECOND), 60),
        60
    ),

    -- Calculate seconds:
    -- Get total seconds difference and convert to minutes (this part formats seconds position)
    DIV(TIMESTAMP_DIFF(ended_at, started_at, SECOND), 60)

  ) AS ride_length,   -- Name of the new calculated column

  -- Create a new column showing the day of the week (e.g., Monday, Tuesday)
  FORMAT_DATE('%A', DATE(started_at)) AS day_of_week

-- Specify the dataset and table to pull data from
FROM `cyclisticcasestudy-482512.cycleuseradata.2020`

-- Filter the data to remove invalid rides
-- This ensures only rides with a positive duration are included
WHERE
  TIMESTAMP_DIFF(ended_at, started_at, SECOND) > 0