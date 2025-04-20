import unittest
import sys
import os

# scripts könyvtár hozzáadása
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

# helyes import
from earnings_data_fetcher import fetch_earnings

class TestFinancialDatasets(unittest.TestCase):
    def test_fetch_earnings(self):
        ticker = "AAL"
        data = fetch_earnings(ticker)
        self.assertIsNotNone(data)
        self.assertIn('press_releases', data)
        self.assertGreater(len(data['press_releases']), 0)

if __name__ == '__main__':
    unittest.main()