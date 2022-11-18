# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:22:49 2022

@author: FOLLOWSM
"""

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"C:\Dev\Projects\Python\sqlite_test\pythonsqlite.db")