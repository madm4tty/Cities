# Cities
Compare city sizes

Background:
I want to be able to supply a target city in an unfamiliar location and be given the nearest city to my location with a similar sized population that I am likely to be familiar with.

Notes:
Data source 
This is a SQLite DB file generated from a csv (city data does not change frequently):
https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000 

Libraries
Pandas - For dataframes
sqlite3 - For DB file
Haversine - Calculate the distance between two points on Earth using their latitude and longitude

Design:
- Get user location (latitude and longitude coordinates in decimal format)
- Take target city from input query
- Lookup target city from SQLite database to confirm unique id code and coordinates
- If there are multiple matches on the name, confirm target country from input
- If there are still multiple matches on the name, default to the city with largest population
- When a single match is obtained, record the id, population and coordinates
- Find the nearest city to the user city with the closest match in population:-
  - create a smaller sub dataframe (sub_df) by constraining by country (and possibly population?)
  - Look into ways to further constraining sub dataframe
  - Loop through dataset and create new column with distance measurement using Haversine from user coordinates
  - Create a score column and populate with the difference between target and city
  - Loop through dataset and determine closest match in population size
  - Return city info
  
  

