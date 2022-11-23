# Cities
Compare city sizes

Background:
I want to be able to supply a target city in an unfamiliar location and be given the nearest city to my location with a similar sized population that I am likely to be familiar with.

Notes:
Data source 
This is a SQLite DB file generated from a csv (city data does not change frequently):
https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000 

Design:
- Get user location (latitude and longitude coordinates in decimal format)
- Take target city from input
- Lookup target city from SQLite database to confirm unique id code and coordinates
- If there are multiple matches, confirm target country from input
- If there are still multiple matches, default to city with largest population
- When a single match is obtained, record the id, population and coordinates
- Find the nearest city to the user location with the closest match in population:-
  - Search the database and match the nearest latitude value
  - Search the database and match the nearest Longitude value
  - Check the population of the city
  - repeat the above until the population matches
  

