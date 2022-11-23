# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:05:53 2022
@author: FOLLOWSM
"""

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
    t_city_df = pd.read_sql(
        "SELECT id, city, country, ctrycode, Timezone, Population, Coordinates FROM cities WHERE city LIKE (?)",
        conn, params=(cityname,))
    return t_city_df



def nearest_city_search(conn, city_id, coords_u):
    print(f"inbound vars - conn:{city_id}, coords_u:{coords_u}")
    
    # split coords
    coords = coords_u.split(",")
    lat, lon = coords[0], coords[1]
    
    
    # Get all cities into DF for lat/long matching
    city_df_lat_lon = pd.read_sql(
        "SELECT id, city, Population, Coordinates FROM cities Limit 10;", conn)
    # Create separate lat lon columns
    city_df_lat_lon[['Lat', 'Lon']] = city_df_lat_lon['Coordinates'].str.split(',', 1, expand=True)
    # Convert lat lon to float datatype to help with sorting
    city_df_lat_lon = city_df_lat_lon.astype({'Lat':'float','Lon':'float'})
    
    
    result = city_df_lat_lon.dtypes
    print("Check city_df_lat_lon datatypes:")
    print(result)
    
    
    # Use the DF to search
    city_match = False
    myint = 0
    while city_match == False:
        myint +=1 # Testing loop
        
    
    
    
    
    
    
    
        
        print(f"Continue the search! ({myint})")
        if myint > 20:
            print("Max loops reached, exit while loop!")
            city_match = True
            
            
    print(city_df_lat_lon)
    
    
    
    # Find nearest match by lat
    latmatch = pd.read_sql(
        "SELECT id, city, Population, Coordinates FROM cities WHERE city LIKE (?)",
        conn, params=(coords_u,))
    #print(f"Latmatch:{latmatch}")
    
          
    print(f"split coords - Lat:{lat}, Lon:{lon}")
    
    
    n_city_id = "TBA"
    return n_city_id




def main():
    pd.set_option('display.max_columns', None)

    database = r"pythonsqlite.db"

    # Local coordinates (testing)
    print('Local coordinates:')
    coords_u = "53.480950, -2.237430"

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
            test = t_result_city['Population'].max()
            print(f"t_result_city: {test}")

            # Sort results by largest population and return first row
            result_city_max = t_result_city.nlargest(1, ['Population'])
            result_city_id = result_city_max.iloc[0]['id']

            print(f"result_city_max: {result_city_max}")
        else:
            # Take row id value for lookup
            result_city_id = t_result_city.iloc[0]['id']
        print("result_city_id: ", result_city_id)
    else:
        # Print results
        result_city_id = t_city_df.iloc[0]['id']
        print("result_city_id: ", result_city_id)


    # Now we've got the target city ID, we need to search
    nearest_city_search(conn, result_city_id, coords_u)




if __name__ == '__main__':
    main()