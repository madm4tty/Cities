# Cities
Compare city sizes

Notes:
Data source 
This is a SQLite DB file generated from a csv (city data does not change frequently):
https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000 

Get user location (latitude and longitude coordinates in decimal format)
Take target city from input
Lookup target city from SQLite database
If there are multiple matches, confirm target country from input
If there are still multiple matches, default to city with largest population
