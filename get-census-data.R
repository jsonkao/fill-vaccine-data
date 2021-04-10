library(dplyr)
library(tidycensus)
library(jsonlite)
census_api_key('b0c03e2d243c837b10d7bb336a998935c35828af')

get_acs(
  state = "Virginia",
  county = c("Richmond city"),
  geography = "block group",
  variables = c(
    income = "B19013_001",
    total_population = "B02001_001",
    white = "B02001_002",
    black = "B02001_003",
    hispanic = "B03002_012",
    asian = "B02001_005"
  )
) %>%
  select(-moe) %>%
  pivot_wider(names_from = variable, values_from = estimate) %>% 
  select(-NAME) %>% 
  toJSON() %>% 
  write('~/Development/census.json')
