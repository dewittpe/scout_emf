import scout
import unittest
import pandas as pd

class TestUtilities(unittest.TestCase):

    def test_ecm_results_class_init(self):
        x = scout.ecm_results("Results_Files_3/ecm_results_1-1.json")
        self.assertIsInstance(x.mas_by_category, pd.DataFrame)
        self.assertIsInstance(x.mas_overall, pd.DataFrame)
        self.assertIsInstance(x.osg_by_category, pd.DataFrame)
        self.assertIsInstance(x.osg_overall, pd.DataFrame)
        self.assertIsInstance(x.financial_metrics, pd.DataFrame)
        self.assertIsInstance(x.filter_variables, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
