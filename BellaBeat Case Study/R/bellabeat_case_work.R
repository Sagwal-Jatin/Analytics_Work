# Install the tidyverse package (collection of packages for data manipulation and visualization)
install.packages('tidyverse')

# Load the tidyverse library into the R environment
library(tidyverse)

# Import the daily activity dataset from a CSV file
daily_activity <- read.csv("dailyActivity_merged.csv")

# Import the sleep dataset from a CSV file
sleep_day <- read.csv("sleepDay_merged.csv")

# Display the first few rows of the daily activity dataset
# This helps us quickly understand the structure and sample data
head(daily_activity)

# Show the column names in the daily activity dataset
# Useful for identifying variables available for analysis
colnames(daily_activity)

# Display the first few rows of the sleep dataset
head(sleep_day)

# Show the column names in the sleep dataset
colnames(sleep_day)

# Count the number of unique users (participants) in the daily activity dataset
# This helps determine how many individuals are included
n_distinct(daily_activity$id)

# Count the number of unique users in the sleep dataset
n_distinct(sleep_day$id)

# Count the total number of rows (records) in the daily activity dataset
# Helps understand dataset size
nrow(daily_activity)

# Count the total number of rows in the sleep dataset
nrow(sleep_day)

# Select key activity variables and generate summary statistics
# Summary includes minimum, maximum, mean, median, etc.
daily_activity %>%
  select(TotalSteps,
         TotalDistance,
         SedentaryMinutes) %>%
  summary()

# Select key sleep variables and generate summary statistics
sleep_day %>%
  select(TotalSleepRecords,
         TotalMinutesAsleep,
         TotalTimeInBed) %>%
  summary()

# Create a scatter plot to visualize the relationship between steps and sedentary minutes
# This helps identify whether more steps are associated with less sedentary time
ggplot(data = daily_activity,
       aes(x = TotalSteps,
           y = SedentaryMinutes)) +
  geom_point()

# Create a bar chart showing sleep records vs minutes asleep
# 'identity' means use actual values from the dataset
# Steelblue is used as the bar color
ggplot(data = sleep_day,
       aes(x = TotalSleepRecords,
           y = TotalMinutesAsleep)) +
  geom_bar(stat = "identity",
           fill = "steelblue")

# Clean and Rename columns before merging
daily_activity_clean <- daily_activity %>%
  rename(date = ActivityDate) %>%
  mutate(date = as.Date(date, format="%m/%d/%Y"))

sleep_day_clean <- sleep_day %>%
  rename(date = SleepDay) %>%
  mutate(date = as.Date(date, format="%m/%d/%Y %I:%M:%S %p"))

# Use an inner_join or full_join for better tidyverse integration
# This matches by BOTH 'Id' and 'date'
combined_data <- daily_activity_clean %>%
  full_join(sleep_day_clean, by = c("Id", "date"))

# Count the number of unique users in the merged dataset
n_distinct(combined_data$Id)

# Count the total number of rows in the merged dataset
nrow(combined_data)

# Display the first few rows of the merged dataset
head(combined_data)

# Show column names in the merged dataset
colnames(combined_data)

# Generate summary statistics for important combined variables
combined_data %>%
  select(TotalMinutesAsleep,
         TotalSteps,
         Calories) %>%
 summary()

# Create a scatter plot to visualize the relationship between sleep and distance traveled
# This helps analyze whether more sleep is associated with higher physical activity
ggplot(data = combined_data,
       aes(x = TotalMinutesAsleep,
           y = TotalDistance)) +
  geom_point()
