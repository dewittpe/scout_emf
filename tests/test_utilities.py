# test_utilities
import scout
import unittest
import pandas as pd

class TestUtilities(unittest.TestCase):

    def test_isfloat_0(self):
        self.assertTrue(scout.isfloat(3.1))

    def test_isfloat_1(self):
        self.assertTrue(scout.isfloat(3))

    def test_isfloat_2(self):
        self.assertFalse(scout.isfloat("a"))

    def test_isfloat_3(self):
        self.assertFalse(scout.isfloat([3.1, 1.8]))

    def test_json_to_df(self):
        df = scout.json_to_df(path = "supporting_data/convert_data/site_source_co2_conversions-ce.json")
        self.assertIsInstance(df, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
