install.packages("tidyverse")
install.packages("janitor")
install.packages("skimr")
install.packages("dplyr")

library(tidyverse)
library(janitor)
library(skimr)
library(dplyr)

amazon_books<-read.csv("bestsellers with categories.csv")

head(amazon_books)
colnames(amazon_books)
str(amazon_books)
summary(amazon_books)
skim(amazon_books)

amazon_books <- clean_names(amazon_books)

colSums(is.na(amazon_books))

nrow(amazon_books)
n_distinct(amazon_books)

amazon_books <- amazon_books %>%
  distinct()

amazon_books <- amazon_books %>%
  mutate(
    user_rating = as.numeric(user_rating),
    reviews = as.numeric(reviews),
    price = as.numeric(price),
    year = as.numeric(year)
  )

amazon_books <- amazon_books %>%
  mutate(
    genre = str_trim(genre)
  )

amazon_books <- amazon_books %>%
  mutate(
    rating_catagory = ifelse(user_rating >= 4.5, "Excellent","Average"),
    price_category = ifelse(price >= 15, "Expensive","Affordable"),
    review_level = ifelse(reviews >= 10000, "High", "Low")
  )

write.csv(amazon_books,"amazon_books_cleaned.csv")

amazon_books %>%
  count(genre)

amazon_books %>%
  group_by(genre) %>%
  summarise(
    average_rating = mean(user_rating)
  )

amazon_books %>%
  group_by(genre) %>%
  summarise(
    average_price = mean(price)
  )

amazon_books %>%
  count(author) %>%
  arrange(desc(n))

amazon_books %>%
  group_by(year) %>%
  summarise(
    average_reviews = mean(reviews)
  )

ggplot(amazon_books, aes(x = genre)) + geom_bar() +
  labs(
    title = "Number of Books by genre",
    x = "Genre",
    y = "Count"
  )

amazon_books %>%
  group_by(genre) %>%
  summarise(avg_rating = mean(user_rating)) %>%
  ggplot(aes(x = genre, y = avg_rating)) +
  geom_col() +
  labs(
    title = "Average Rating by Genre"
  )

amazon_books %>%
  group_by(year) %>%
  summarise(avg_price = mean(price)) %>%
  ggplot(aes(x = year, y = avg_price)) +
  geom_line()+
  labs(
    title = "Average Price Over Time"
  )

amazon_books %>%
  count(author) %>%
  arrange(desc(n)) %>%
  slice_head(n =  10) %>%
  ggplot(aes(x = reorder(author, n), y = n)) +
  geom_col() +
  coord_flip()

genre_summary <- amazon_books %>%
  group_by(genre) %>%
  summarise(
    average_rating = mean(user_rating),
    average_price = mean(price),
    total_books = n()
  )

write.csv(
    genre_summary,
    "genre_summary.csv"
)
