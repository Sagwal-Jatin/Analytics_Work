-- Combine cleaned trip data from 2019 and 2020 into one unified dataset

SELECT
  -- Convert trip_id to STRING to ensure both tables have the same data type
  CAST(trip_id AS STRING) AS trip_id,

  usertype,        -- Rider category from the 2019 dataset (Subscriber or Customer)

  ride_length,     -- Duration of the ride (already calculated in HH:MM:SS)

  day_of_week      -- Day name extracted from the ride start date

FROM
  -- Source table containing cleaned 2019 trip data
  `cyclisticcasestudy-482512.cycleuseradata.2019_cleaned`

UNION ALL

SELECT
  -- Convert ride_id to STRING so it matches the data type of trip_id
  CAST(ride_id AS STRING) AS trip_id,

  -- Standardize rider categories for consistency across datasets
  CASE
    -- Convert values to lowercase to avoid case sensitivity issues
    WHEN LOWER(member_casual) IN ('member', 'subscriber') THEN 'Subscriber'
    WHEN LOWER(member_casual) IN ('casual', 'customer') THEN 'Customer'

    -- Keep original value if it does not match known categories
    ELSE member_casual
  END AS usertype,

  ride_length,     -- Duration of the ride

  day_of_week      -- Day of the week for analysis

FROM
  -- Source table containing cleaned 2020 trip data
  `cyclisticcasestudy-482512.cycleuseradata.2020_cleaned`;