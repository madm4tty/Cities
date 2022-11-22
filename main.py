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


def iterate_over_df_result():
    # Empty for now
    return





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
        input_country = input("Which country is the city in? (use country code):")
        input_country = input_country.upper()
        print(f"input_country is: {input_country}")

        t_result_city = t_city_df.query("ctrycode == @input_country")

        # If there are multiple cities in results, the city with the largest population will be used
        t_result_city_len = (len(t_result_city.index))
        print(f"t_result_city_len is: {t_result_city_len}")
        if t_result_city_len > 1:
            #t_result_city
            
            
            print(f"Multiple cities found for {input_country} (see below), defaulting to city with largest population")
            print(t_result_city)
            
            #recent_date = df['date'].max()
            #result_city_max = t_result_city['Population'].max()
            
            test = t_result_city['Population'].max()
            print (f"t_result_city: {test}")
            
            # top n rows ordered by multiple columns
           # gapminder_2007.nlargest(3,['lifeExp','gdpPercap'])
            #gapminder_2007.nlargest(3,['lifeExp','gdpPercap'])
            result_city_max = t_result_city.nlargest(1,['Population'])
            
            #for row in t_result_city.index:
                #print(f'Max element of row {row} is:', max(t_result_city.iloc[row]))
             #   print(f'Max element of row {row} is:', max(t_result_city.iloc[row]))
            
            
            #result_city_max = t_result_city.loc[t_result_city['Population'].max(), 'id']
            #result_city_max = df.loc[df.groupby('YearReleased')['count'].idxmax()]
           
            # result_city_max = t_result_city.loc[t_result_city['Population'].idxmax()]
            #result_city_id = result_city_max.iloc[0]['id']
            
            #df2=df.loc[df['Fee'] == 30000, 'Courses']

            #df2=df.loc[df['Fee'] == 30000, 'Courses']

            
            print(f"result_city_max: {result_city_max}")
            
            #result_city_id = result_city_max.iloc[0]['id']
            #result_city_id = ['Population'].max()


        else:
            # Take row id value for lookup
            result_city_id = t_result_city.iloc[0]['id']
            


        #print("result_city_id: ", result_city_id)


    else:
        # Print results
        print("t_city_df_len is:", t_city_df_len)
        print(t_city_df)




if __name__ == '__main__':
    main()