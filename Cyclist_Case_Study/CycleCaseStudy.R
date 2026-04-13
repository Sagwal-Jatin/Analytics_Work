# Load required libraries for data manipulation and conflict management
library(tidyverse)
library(conflicted)

# Import datasets for Q1 2019 and Q1 2020 bike trips
q1_2019 <- read_csv("Divvy_trips_2019_Q1.csv")
q1_2020 <- read_csv("Divvy_Trips_2020_Q1.csv")

# View column names in both datasets to identify differences
colnames(q1_2019)
colnames(q1_2020)

# Rename columns in 2019 dataset so that both datasets have consistent column names
# This is required before combining (stacking) datasets
(q1_2019 <- rename(q1_2019
,ride_id = trip_id
,rideable_type = bikeid
,started_at = start_time
,ended_at = end_time
,start_station_name = from_station_name
,start_station_id = from_station_id
,end_station_name = to_station_name
,end_station_id = to_station_id
,member_casual = usertype
))

# Check structure of both datasets (data types and variables)
str(q1_2019)
str(q1_2020)


# Convert ride_id and rideable_type to character type
# This ensures both datasets have matching data types before merging
q1_2019 <- mutate(q1_2019, ride_id = as.character(ride_id)
,rideable_type = as.character(rideable_type))


# Combine (stack) the two quarterly datasets into one dataset
# bind_rows() appends rows from one dataset to another
all_trips <- bind_rows(q1_2019, q1_2020)

# Remove columns that are no longer available in 2020 data
# This keeps dataset consistent and avoids errors in analysis
all_trips <- all_trips %>%
select(-c(start_lat, start_lng, end_lat, end_lng, birthyear, gender, "tripduration"))

# Inspect the combined dataset
colnames(all_trips)   # Display column names
nrow(all_trips)       # Count number of rows
dim(all_trips)        # Show rows and columns
head(all_trips)       # Preview first 6 rows
str(all_trips)        # Check structure and data types
summary(all_trips)    # Get statistical summary

# Standardize user types
# Convert old labels into consistent categories
all_trips <- all_trips %>%
mutate(member_casual = recode(member_casual
,"Subscriber" = "member"
,"Customer" = "casual"))

# Create new date-related variables for analysis
all_trips$date <- as.Date(all_trips$started_at)
all_trips$month <- format(as.Date(all_trips$date), "%m")
all_trips$day <- format(as.Date(all_trips$date), "%d")
all_trips$year <- format(as.Date(all_trips$date), "%Y")
all_trips$day_of_week <- format(as.Date(all_trips$date), "%A")

# Calculate ride duration by subtracting start time from end time
all_trips$ride_length <- difftime(all_trips$ended_at,all_trips$started_at)

# Check updated dataset structure
str(all_trips)

# Convert ride_length into numeric format for calculations
all_trips$ride_length <- as.numeric(as.character(all_trips$ride_length))

# Verify ride_length is numeric
is.numeric(all_trips$ride_length)

# Clean dataset by removing:
# 1. Test station rides (HQ QR)
# 2. Negative ride durations (data errors)
all_trips_v2 <- all_trips[!(all_trips$start_station_name == "HQ QR" | all_trips$ride_length<0),]

# Calculate descriptive statistics for ride duration
mean(all_trips_v2$ride_length)    # Average ride time
median(all_trips_v2$ride_length)  # Middle value
max(all_trips_v2$ride_length)     # Longest ride
min(all_trips_v2$ride_length)     # Shortest ride

# Summary statistics
summary(all_trips_v2$ride_length)

# Compare ride duration between members and casual users
aggregate(all_trips_v2$ride_length ~ all_trips_v2$member_casual, FUN = mean)
aggregate(all_trips_v2$ride_length ~ all_trips_v2$member_casual, FUN = median)
aggregate(all_trips_v2$ride_length ~ all_trips_v2$member_casual, FUN = max)
aggregate(all_trips_v2$ride_length ~ all_trips_v2$member_casual, FUN = min)
aggregate(all_trips_v2$ride_length ~ all_trips_v2$member_casual + all_trips_v2$day_of_week,
FUN = mean)

# Calculate average ride duration by user type and day of week
aggregate(all_trips_v2$ride_length ~ all_trips_v2$member_casual + all_trips_v2$day_of_week,
FUN = mean)


# Fix ordering of weekdays for proper visualization
all_trips_v2$day_of_week <- ordered(all_trips_v2$day_of_week, levels=c("Sunday", "Monday",
"Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"))

# Recalculate average ride duration with ordered weekdays
aggregate(all_trips_v2$ride_length ~ all_trips_v2$member_casual + all_trips_v2$day_of_week,
FUN = mean)

# Create summarized dataset showing:
# Number of rides
# Average ride duration
# Grouped by user type and weekday
all_trips_v2 %>%
mutate(weekday = wday(started_at, label = TRUE)) %>%
  group_by(member_casual, weekday) %>%
  summarise(number_of_rides = n()
,average_duration = mean(ride_length)) %>%
+   arrange(member_casual, weekday)

# Visualization 1:
# Number of rides per weekday by user type
all_trips_v2 %>%
mutate(weekday = wday(started_at, label = TRUE)) %>%
group_by(member_casual, weekday) %>%
summarise(number_of_rides = n()
,average_duration = mean(ride_length)) %>%
arrange(member_casual, weekday) %>%
ggplot(aes(x = weekday, y = number_of_rides, fill = member_casual)) +
geom_col(position = "dodge")

# Visualization 2:
# Average ride duration per weekday by user type
all_trips_v2 %>%
mutate(weekday = wday(started_at, label = TRUE)) %>%
group_by(member_casual, weekday) %>%
summarise(number_of_rides = n()
,average_duration = mean(ride_length)) %>%
arrange(member_casual, weekday) %>%
ggplot(aes(x = weekday, y = average_duration, fill = member_casual)) +
geom_col(position = "dodge")

# Export summarized results to CSV file
counts <- aggregate(all_trips_v2$ride_length ~ all_trips_v2$member_casual +
all_trips_v2$day_of_week, FUN = mean)
write.csv(counts, file = 'avg_ride_length.csv')