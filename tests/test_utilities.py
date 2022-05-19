# test_utilities
import scout
import unittest
import pandas as pd
import json

class TestUtilities(unittest.TestCase):

    def test_isfloat_0(self):
        self.assertTrue(scout.isfloat(3.1))

    def test_isfloat_1(self):
        self.assertTrue(scout.isfloat(3))

    def test_isfloat_2(self):
        self.assertFalse(scout.isfloat("a"))

    def test_isfloat_3(self):
        self.assertFalse(scout.isfloat([3.1, 1.8]))

    def test_json_to_df_0(self):
        # expect error if data and path are provided
        p = "supporting_data/convert_data/site_source_co2_conversions-ce.json"
        f = open(p, "r")
        d = json.load(f)
        f.close()
        self.assertRaises(AssertionError, scout.json_to_df, data = d, path = p)

    def test_json_to_df_1(self):
        # test requiring reading from a file
        df = scout.json_to_df(path = "supporting_data/convert_data/site_source_co2_conversions-ce.json")
        self.assertIsInstance(df, pd.DataFrame)

    def test_json_to_df_2(self):
        # test using json data
        f = open("supporting_data/convert_data/site_source_co2_conversions-ce.json", "r")
        d = json.load(f)
        f.close()
        df = scout.json_to_df(data = d)
        self.assertIsInstance(df, pd.DataFrame)

    def test_mapping_blg_type_to_class(self):
        expected = \
                pd.DataFrame(data = {
                    "assembly" : "Commercial",
                    "education" : "Commercial",
                    "food sales" : "Commercial",
                    "food service" : "Commercial",
                    "health care" : "Commercial",
                    "lodging" : "Commercial",
                    "large office" : "Commercial",
                    "small office" : "Commercial",
                    "mercantile/service" : "Commercial",
                    "warehouse" : "Commercial",
                    "other" : "Commercial",
                    "single family home" : "Residential",
                    "multi family home" : "Residential",
                    "mobile home" : "Residential"
                    }.items()
                    , columns = ["building_type", "building_class"])
        df = scout.mapping_variables()
        self.assertTrue(all(df.building_type_to_class == expected))

if __name__ == "__main__":
    unittest.main()

