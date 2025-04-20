import unittest
import sys
import os

# Hozzáadjuk a scripts könyvtárat a PYTHONPATH-hoz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from market_data import get_stock_price, get_forex_rate, get_commodity_price

class TestMarketData(unittest.TestCase):

    def test_stock_price_fmp(self):
        price = get_stock_price("AAPL")
        self.assertIsNotNone(price)
        self.assertGreater(price, 0)

    def test_stock_price_alpha(self):
        price = get_stock_price("AAPL", api="alpha")
        self.assertIsNotNone(price)
        self.assertGreater(price, 0)

    def test_forex_rate_fmp(self):
        rate = get_forex_rate("EURUSD")
        self.assertIsNotNone(rate)
        self.assertGreater(rate, 0)

    def test_forex_rate_alpha(self):
        rate = get_forex_rate("EURUSD", api="alpha")
        self.assertIsNotNone(rate)
        self.assertGreater(rate, 0)

    def test_commodity_price_fmp(self):
        price = get_commodity_price("XAUUSD")
        self.assertIsNotNone(price)
        self.assertGreater(price, 0)

if __name__ == '__main__':
    unittest.main()