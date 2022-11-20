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
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """

    cur = conn.cursor()

    # Query target city
    t_city_df = pd.read_sql(
        "SELECT id, city, country, ctrycode, Timezone, Population, Coordinates FROM cities WHERE city LIKE (?)",
        conn, params=(cityname,))

    # rows = cur.fetchall()
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
        u_city_df = select_cities(conn, coords_u)

    t_city_df_len = (len(t_city_df.index))

    # If there are multiple results in t_city_df we need to narrow down
    if t_city_df_len > 1:
        print("t_city_df:")
        print(t_city_df)
        msg = f"There are: {t_city_df_len} results for: {t_city_input}."
        print(msg)
        input_country = input("Which country is the city in? (use country code):")
        input_country.capitalize()

        #result_city_df = t_city_df.loc[t_city_df.ctrycode == input_country].city
        #result_city_id = [t_city_df.ctrycode == input_country].id

        #result_city_id = df.loc[df['column_name'] == some_value]
        #result_city_id = t_city_df.loc[t_city_df['ctrycode'] == input_country]
        #df.loc[df['favorite_color'] == 'yellow']
        result_city_id = t_city_df.query("ctrycode == GB")

        #df.loc[df['column_name'].isin(some_values)]
        #result_city_id = t_city_df.loc[t_city_df['ctrycode'].isin(input_country)]

        print("result_city_id: ", result_city_id)

        # If there are multiple cities left after confirming country, the city with the largest population will be used

        # for ind in result_city_df.index:
        #    # call iterate_over_df_result function at this point?
        #    print(result_city_df.row["city"])

        # iterate through each row and select
        # 'Name'  and 'Stream' column respectively.
        # for ind in result_city_df.index:
        #    print(result_city_df['city'][ind], result_city_df['country'][ind])

        #print(result_city_df)
        # print(t_city_df.loc[result_city_df])

        # print(t_city_df.loc[t_city_df.country == input_country].city)
    else:
        # Print results
        print("t_city_df_len is:", t_city_df_len)
        print(t_city_df)

    # Print results
    # print(t_city_df)


if __name__ == '__main__':
    main()
