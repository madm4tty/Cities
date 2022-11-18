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

    

    #Query target city
    TcityDF = pd.read_sql("SELECT \"ASCII Name\", \"Country Name EN\", Population, Coordinates FROM cities WHERE \"ASCII Name\" = (?)",conn ,params=(cityname,))



    #rows = cur.fetchall()
    return TcityDF




def main():
    database = r"C:\Dev\Projects\Python\sqlite_test\pythonsqlite.db"    
    
    #Local coordinates (testing)
    print('Local coordinates:')
    coords_U = "53.480950, -2.237430"

    #Get target city
    print('Enter search city:')
    Tcityinput = input()
    

    print ("Searching for:",Tcityinput)


    # create a database connection
    conn = create_connection(database)
    with conn:
       TcityDF = select_cities(conn, Tcityinput)
       UcityDF = select_cities (conn, coords_U)


    TcityDF_len = (len(TcityDF.index))

    print(TcityDF_len, " results found:")

    print(TcityDF)

       
        

if __name__ == '__main__':
    main()