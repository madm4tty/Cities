import unittest
from math import radians
import pandas as pd
import sqlite3

# Import the functions from your original script
from main import create_connection, select_cities, haversine, get_user_ctrycode, nearest_city_search

class TestYourScript(unittest.TestCase):

    def test_create_connection(self):
        conn = create_connection(':memory:')
        self.assertIsInstance(conn, sqlite3.Connection)

    def test_select_cities(self):
        conn = create_connection(':memory:')
        with conn:
            # Create an example table and insert data for testing
            conn.execute('''CREATE TABLE cities (id INTEGER PRIMARY KEY, city TEXT, country TEXT, ctrycode TEXT, Timezone TEXT, Population INTEGER, Coordinates TEXT)''')
            conn.execute('''INSERT INTO cities (city, country, ctrycode, Timezone, Population, Coordinates) VALUES ('Test City', 'Test Country', 'TC', 'UTC', 50000, '0,0')''')

            result = select_cities(conn, 'Test City')
            self.assertIsNotNone(result)
            self.assertEqual(result.iloc[0]['city'], 'Test City')

    def test_haversine(self):
        lon1, lat1 = radians(0), radians(0)
        lon2, lat2 = radians(0), radians(0)
        result = haversine(lon1, lat1, lon2, lat2)
        self.assertEqual(result, 0)

    def test_get_user_ctrycode(self):
        df = pd.DataFrame({'lat': [0], 'lon': [0], 'ctrycode': ['TC']})
        lat, lon = 0, 0
        result = get_user_ctrycode(df, lat, lon)
        self.assertEqual(result['ctrycode'], 'TC')

    def test_nearest_city_search(self):
        conn = create_connection("pythonsqlite.db")
        test_cases = [
            (10119, "53.798921,-1.551878", 100000, 500),  # Normal case
            (52131, "53.798921,-1.551878", 198293, 10),   # Edge case: small search radius
            # Add more test cases as needed
        ]

        for city_id, coords_u, pop_t, searchRadius in test_cases:
            result = nearest_city_search(conn, city_id, coords_u, pop_t, searchRadius)
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
