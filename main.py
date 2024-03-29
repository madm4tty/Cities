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
    try:
        # Query target city
        cityname = cityname.lower()
        t_city_df = pd.read_sql(
            "SELECT id, city, country, ctrycode, Timezone, Population, Coordinates FROM cities WHERE city LIKE (?)",
            conn, params=(cityname,))
        return t_city_df
    
    except Exception as e:
        print(f"An error occurred while querying the city: {e}")
        return None

def haversine(lon1, lat1, lon2, lat2):
    try:
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
    
    except Exception as e:
        print(f"An error occurred while calculating the haversine distance: {e}")
        return None

def get_user_ctrycode(df, lat, lon):
    try:
        print(f"get_user_ctrycode: lat:{lat}, lon:{lon}")
        dist = (df['lat'] - lat).abs() + (df['lon'] - lon).abs()
        print(f"dist value: {dist}")
        return df.loc[dist.idxmin()]
    
    except Exception as e:
        print(f"An error occurred while getting the user's country code: {e}")
        return None


def nearest_city_search(conn, city_id, coords_u, pop_t, searchRadius):
    try:
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
        city_df_lat_lon[['Lat', 'Lon']] = city_df_lat_lon['Coordinates'].str.split(pat=',', n=1, expand=True)

        # Convert lat lon to float datatype to allow processing
        city_df_lat_lon = city_df_lat_lon.astype({'Lat': 'float', 'Lon': 'float'})
    
        # Narrow down dataset by population bands
        if pop_t > 1000000:
            pophigh = city_df_lat_lon['Population'].max()
            poplow = 1000000
        elif 500000 <= pop_t <= 1000000:
            pophigh = 1000000
            poplow = 500000
        elif 100000 <= pop_t <= 500000:
            pophigh = 500000
            poplow = 100000
        elif 50000 <= pop_t <= 100000:
            pophigh = 100000
            poplow = 50000
        elif 5000 <= pop_t <= 10000:
            pophigh = 10000
            poplow = 5000
        else:
            pophigh = 5000
            poplow = city_df_lat_lon['Population'].min()
            
        """ Use Decimal Degree calc to narrow results
        Approx 111km (60 miles) to each degree, calculate radius 
        based on searchRadius variable
        """
        diffDegrees = (searchRadius + 200) / 111
        latH = u_lat + diffDegrees
        latL = u_lat - diffDegrees
        lonH = u_lon + diffDegrees
        lonL = u_lon - diffDegrees
        sub_df = (city_df_lat_lon.loc[(city_df_lat_lon['Lat'] >= latL) & 
                                      (city_df_lat_lon['Lat'] <= latH) & 
                                      (city_df_lat_lon['Lon'] >= lonL) & 
                                      (city_df_lat_lon['Lon'] <= lonH) &
                                      (city_df_lat_lon['Population'] >= poplow) &
                                      (city_df_lat_lon['Population'] <= pophigh)])
    
        # Create new empty column in sub_df for calculated distances
        sub_df=sub_df.assign(distance = '')
        sub_df=sub_df.assign(score = '')
        sub_df=sub_df.assign(finalscore = '')
    
        # Populate distance and score column in sub_df
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
    
        # Remove any results that are too far away > {searchRadius}km
        sub_df = sub_df[sub_df.distance < searchRadius]
    
        # Sort by final score to get best match
        sub_df_sorted = sub_df[sub_df['score'] != 0].sort_values(['finalscore'])
    
        #sub_df_sorted.to_csv('sub_df_sorted.csv')
    
        # Populate variables for return
        n_city_id = sub_df_sorted.iloc[0]['id']
        n_city_name = sub_df_sorted.iloc[0]['city']
        n_city_country = sub_df_sorted.iloc[0]['country']
        n_city_pop = sub_df_sorted.iloc[0]['Population']
        n_city_dist = sub_df_sorted.iloc[0]['distance']
    
        #(len(t_result_city.index)
        print(f"sub_df_sorted length: {len(sub_df_sorted.index)}")
        print(sub_df_sorted[['city', 'country', 'Population', 'distance']].head(10))
    
        return n_city_id, n_city_name, n_city_country, n_city_pop, n_city_dist
    
    except Exception as e:
        print(f"An error occurred while searching for the nearest city: {e}")
        return None

def main():
    try:
        pd.set_option('display.max_columns', None)
        database = r"pythonsqlite.db"

        # Local coordinates (testing) - Get from user location eventually
        #print('Local coordinates:')
        coords_u = "53.798921,-1.551878"  # - Leeds
        distThreshold = 200
        searchRadius = 500

        # Get target city
        print('Enter search city:')
        t_city_input = input()

        print("Searching for:", t_city_input)

        # create a database connection
        conn = create_connection(database)
        with conn:
            t_city_df = select_cities(conn, t_city_input)

        t_city_df_len = (len(t_city_df.index))

        if t_city_df_len == 0:
            print(f"City not found: {t_city_input}")
            return

        # If there are multiple results in t_city_df we need to narrow down
        if t_city_df_len > 1:

            msg = f"There are: {t_city_df_len} results for: {t_city_input}:"
            print(msg)
            print(t_city_df[['city', 'country', 'ctrycode', 'Population']])
            input_country = input("Which country is the city in? (use country code eg:GB):")
            input_country = input_country.upper()
            print(f"input_country is: {input_country}")

            t_result_city = t_city_df.query("ctrycode == @input_country")

            # If there are multiple cities in results, the city with the largest population will be used
            t_result_city_len = (len(t_result_city.index))
            if t_result_city_len > 1:
                print(f"Multiple cities found for {input_country} (see below), defaulting to city with largest population")
                print(t_result_city)
                pop_t = t_result_city['Population'].max()
                # Sort results by largest population and return first row
                result_city_max = t_result_city.nlargest(1, ['Population'])
                print(f"result_city_max: {result_city_max}")
                result_city_id = result_city_max.iloc[0]['id']
                city_t_country = result_city_max.iloc[0]['country']
                print(f"result_city_id: {result_city_id}")
            else:
                # Take row id value for lookup
                pop_t = t_result_city.iloc[0]['Population']
                result_city_id = t_result_city.iloc[0]['id']
                city_t_country = t_result_city.iloc[0]['country']
                
        else:
            # Print results
            result_city_id = t_city_df.iloc[0]['id']
            pop_t = t_city_df.iloc[0]['Population']
            city_t_country = t_city_df.iloc[0]['country']

        # Get target city's name
        city_t_name = t_city_df.iloc[0]['city']


        print(f"Target city is: {city_t_name}, {city_t_country} with a population of: {pop_t}")

        # Now run the search passing in the variables
        n_city_id, n_city_name, n_city_country, n_city_pop, n_city_dist = \
        nearest_city_search(conn, result_city_id, coords_u, pop_t, searchRadius)

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
            Nearest town/city within {searchRadius}km with a similar population: {n_city_name}, {n_city_country}
            Population: {n_city_pop}
            Distance from your location(km):{n_city_dist}
            
            """
        print(returnedData)

        print("End of Main script")

    except Exception as e:
        print(f"An error occurred while running the main script: {e}")
        
if __name__ == '__main__':
    main()