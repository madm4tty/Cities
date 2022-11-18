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



def get_col_names(conn):
#this works beautifully given that you know the table name
    cur = conn.cursor()
    
    
    print ([member[0] for member in cur.description])



def select_cities(conn, cityname):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """

    cur = conn.cursor()

    #headers = list(map(lambda attr : attr[0], cur.description))
    #results = [{header:row[i] for i, header in enumerate(headers)} for row in cursor]

    #cur.execute("SELECT * FROM cities WHERE \"ASCII Name\" = ?", (cityname,))

    #Select useful columns
    #cur.execute("SELECT \"ASCII Name\", \"Country Name EN\", Population, Coordinates FROM cities WHERE \"ASCII Name\" = ?", (cityname,))
    
    #citDF = pd.read_sql("SELECT \"ASCII Name\", \"Country Name EN\", Population, Coordinates FROM cities WHERE \"ASCII Name\" = (?)",conn ,params=(cityname,))
    citDF = pd.read_sql("SELECT * FROM cities WHERE \"ASCII Name\" = (?)",conn ,params=(cityname,))



    #rows = cur.fetchall()
    return citDF




def main():
    database = r"C:\Dev\Projects\Python\sqlite_test\pythonsqlite.db"
    #con = sqlite3.connect('/Users/mac/Desktop/Python/Baye_stat/productiondisruption/PCI_meat.sqlite')
    
    #Get target city
    print('Enter search city:')
    cityinput = input()
    
    #TESTING ONLY
    #cityinput = 'Leeds'

    print ("Searching for:",cityinput)


    # create a database connection
    conn = create_connection(database)
    with conn:
       citDF = select_cities(conn, cityinput)

    print(citDF)


    #for row in rows:
     #   print(row)
        
        
        

if __name__ == '__main__':
    main()