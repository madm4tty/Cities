# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:22:49 2022

@author: FOLLOWSM
"""


import pandas as pd
import sqlite3 as sql3

# Read a csv file to a dataframe with custom delimiter
myDf =  pd.read_csv('C:\Dev\Projects\Python\Data\geonames-all-cities-with-a-population-1000.csv', sep=';'  , engine='python')


del myDf['Geoname ID']
del myDf['Name']
del myDf['Alternate Names']
del myDf['Feature Class']
del myDf['Feature Code']
del myDf['Admin1 Code']
del myDf['Admin2 Code']
del myDf['Admin3 Code']
del myDf['Admin4 Code']
del myDf['LABEL EN']


print('Contents of Dataframe : ')


print(myDf)
print(myDf.dtypes)

#Push to SQLite file
conn = sql3.connect('C:\Dev\Projects\Python\sqlite_test\pythonsqlite.db')
myDf.to_sql('cities', conn, if_exists='replace', index=False)
pd.read_sql('select * from cities', conn)