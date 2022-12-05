# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:05:53 2022
@author: FOLLOWSM
"""

from math import radians, cos, sin, asin, sqrt
import pandas as pd
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_cities(conn, cityname):
    # Query target city
    cityname = cityname.lower()
    t_city_df = pd.read_sql(
        "SELECT id, city, country, ctrycode, Timezone, Population, Coordinates FROM cities WHERE city LIKE (?)",
        conn, params=(cityname,))
    return t_city_df

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def get_user_ctrycode(df, lat, lon):
    print(f"get_user_ctrycode:lat:{lat}, lon:")
    dist = (df['lat'] - lat).abs() + (df['lon'] - lon).abs()
    print(f"dist value: {dist}")
    return df.loc[dist.idxmin()]


def nearest_city_search(conn, city_id, coords_u, pop_t):
    #print(f"inbound vars - conn:{city_id}, coords_u:{coords_u}, pop_t:{pop_t}")

    # split coords
    u_coords = coords_u.split(",")
    u_lat, u_lon = u_coords[0], u_coords[1]

    # convert coords to float 64 datatype
    u_lat = float(u_lat)
    u_lon = float(u_lon)
    #print(f"split coords - u_Lat:{u_lat}, u_Lon:{u_lon}")

    # Get all cities into DF for lat/long matching
    city_df_lat_lon = pd.read_sql(
        "SELECT id, city, country, ctrycode, Population, Coordinates FROM cities;", conn)

    # Create separate lat lon columns
    city_df_lat_lon[['Lat', 'Lon']] = city_df_lat_lon['Coordinates'].str.split(',', 1, expand=True)

    # Convert lat lon to float datatype to allow processing
    city_df_lat_lon = city_df_lat_lon.astype({'Lat': 'float', 'Lon': 'float'})
    #result = city_df_lat_lon.dtypes
    #print("Check city_df_lat_lon datatypes:")
    #print(result)

    # Get subset of main dataframe for sort and search
    #print("Get subset of main dataframe for sort and search")    
    # Narrow down dataset by population bands
    if pop_t > 500000:
        pophigh = pop_t + 500000
        poplow = pop_t - 500000
    elif 100000 <= pop_t <= 500000:
        pophigh = pop_t + 50000
        poplow = pop_t - 50000
    elif 50000 <= pop_t <= 100000:
        pophigh = pop_t + 5000
        poplow = pop_t - 5000
    elif 5000 <= pop_t <= 10000:
        pophigh = pop_t + 500
        poplow = pop_t - 500
    else:
        pophigh = pop_t + 50
        poplow = pop_t - 50
        
    # Narrow by population - Country code allows nearest city?
    sub_df = city_df_lat_lon.loc[(city_df_lat_lon['ctrycode'] == "GB")]
    #sub_df = city_df_lat_lon.loc[(city_df_lat_lon['Population'] > poplow) & (city_df_lat_lon['Population'] < pophigh)]
   
    # Create new empty column in sub_df for calculated distances
    sub_df=sub_df.assign(distance = '')
    sub_df=sub_df.assign(score = '')
    sub_df=sub_df.assign(finalscore = '')
    
    # Populate distance and score column in sub_df
    #print("Populate distance column in sub_df")
    # iterate through each row and select
    for ind in sub_df.index:
        t_lat = (sub_df['Lat'][ind])
        t_lon = (sub_df['Lon'][ind])
        t_pop = (sub_df['Population'][ind])
        distance = haversine(u_lat, u_lon, t_lat, t_lon)
        t_pop = int(t_pop)
        distance = int(distance)
        sub_df.loc[ind,'distance'] = distance
        score = abs(pop_t-t_pop)
        sub_df.loc[ind,'score'] = score
        finalscore = int(distance + score)
        sub_df.loc[ind,'finalscore'] = finalscore

    sub_df=sub_df.astype({'distance': 'int', 'score': 'int', 'finalscore': 'int'})
    # Update datatypes and check
    #result = sub_df.dtypes
    #print("Check sub_df datatypes:")
    #print(result)
    
    # Sort by
    sub_df_sorted = sub_df[sub_df['score'] != 0].sort_values(['finalscore'])
    
    #sub_df_sorted.to_csv('sub_df_sorted.csv')
    
    # Populate
    n_city_id = sub_df_sorted.iloc[0]['id']
    n_city_name = sub_df_sorted.iloc[0]['city']
    n_city_country = sub_df_sorted.iloc[0]['country']
    n_city_pop = sub_df_sorted.iloc[0]['Population']
    n_city_dist = sub_df_sorted.iloc[0]['distance']

    print("print sub_df_sorted")
    print(sub_df_sorted)
    print("End of nearest_city_search")

    return n_city_id, n_city_name, n_city_country, n_city_pop, n_city_dist

def main():
    pd.set_option('display.max_columns', None)
    database = r"pythonsqlite.db"

    # Local coordinates (testing) - Get from user location eventually
    #print('Local coordinates:')
    coords_u = "53.798921,-1.551878"  # - Leeds
    distThreshold = 200

    # Get target city
    print('Enter search city:')
    t_city_input = input()

    print("Searching for:", t_city_input)

    # create a database connection
    conn = create_connection(database)
    with conn:
        t_city_df = select_cities(conn, t_city_input)

    t_city_df_len = (len(t_city_df.index))

    # If there are multiple results in t_city_df we need to narrow down
    if t_city_df_len > 1:
        print("t_city_df:")
        print(t_city_df)
        msg = f"There are: {t_city_df_len} results for: {t_city_input}."
        print(msg)
        input_country = input("Which country is the city in? (use country code eg:GB):")
        input_country = input_country.upper()
        print(f"input_country is: {input_country}")

        t_result_city = t_city_df.query("ctrycode == @input_country")

        # If there are multiple cities in results, the city with the largest population will be used
        t_result_city_len = (len(t_result_city.index))
        print(f"t_result_city_len is: {t_result_city_len}")
        if t_result_city_len > 1:
            print(f"Multiple cities found for {input_country} (see below), defaulting to city with largest population")
            print(t_result_city)
            pop_t = t_result_city['Population'].max()
            print(f"pop_t in if: {pop_t}")

            # Sort results by largest population and return first row
            result_city_max = t_result_city.nlargest(1, ['Population'])
            print(f"result_city_max: {result_city_max}")
            result_city_id = result_city_max.iloc[0]['id']
            print(f"result_city_id: {result_city_id}")

        else:
            # Take row id value for lookup
            pop_t = t_result_city.iloc[0]['Population']
            print(f"pop_t in else: {pop_t}")
            result_city_id = t_result_city.iloc[0]['id']
            #print("result_city_id in else: ", result_city_id)
    else:
        # Print results
        result_city_id = t_city_df.iloc[0]['id']
        pop_t = t_city_df.iloc[0]['Population']
        #print("result_city_id: ", result_city_id)

    # Get target city's name
    city_t_name = t_city_df.iloc[0]['city']

    print(f"Target city is: {city_t_name} with a population of: {pop_t}")
    
    # Now run the search passing in the variables
    n_city_id, n_city_name, n_city_country, n_city_pop, n_city_dist = nearest_city_search(conn, result_city_id, coords_u, pop_t)
    
    #Return info
    if n_city_dist < distThreshold:
        returnedData = f"""
        Town/City supplied: {city_t_name}
        Population: {pop_t}
        
        Nearest local town/city: {n_city_name}
        Population: {n_city_pop}
        Distance from your location(km):{n_city_dist}
        
        """
    else:
        returnedData = f"""
        Town/City supplied: {city_t_name}
        Population: {pop_t}
        
        No locations found within {distThreshold}km of your location.
        Nearest town/city with a similar population: {n_city_name}, {n_city_country}
        Population: {n_city_pop}
        Distance from your location(km):{n_city_dist}
        
        """
    print(returnedData)

    print("End of Main script")


if __name__ == '__main__':
    main()