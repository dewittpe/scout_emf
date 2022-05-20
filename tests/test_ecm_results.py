import scout
import unittest
import pandas as pd

class TestUtilities(unittest.TestCase):

    def test_ecm_results_class_init(self):
        x = scout.ecm_results(path = "Results_Files_3/ecm_results_1-1.json.gz")
        self.assertIsInstance(x.mas_by_category, pd.DataFrame)
        self.assertIsInstance(x.mas_overall, pd.DataFrame)
        self.assertIsInstance(x.osg_by_category, pd.DataFrame)
        self.assertIsInstance(x.osg_overall, pd.DataFrame)
        self.assertIsInstance(x.financial_metrics, pd.DataFrame)
        self.assertIsInstance(x.filter_variables, pd.DataFrame)

    def test_aggregate_for_emf(self):
        x = scout.ecm_results(path = "Results_Files_3/ecm_results_2.json.gz")
        self.assertIsNone(x.emf_aggregation)
        x.aggregate_for_emf()
        self.assertIsInstance(x.emf_aggregation, pd.DataFrame)

    def test_by_category_vs_overall(self):
        x = scout.ecm_results(path = "Results_Files_3/ecm_results_1-1.json.gz")
        self.assertIsNone(x.by_category_aggreation_vs_overall)
        x.by_category_vs_overall()
        self.assertIsInstance(x.by_category_aggreation_vs_overall, dict)
        self.assertIsInstance(x.by_category_aggreation_vs_overall["Markets and Savings"], pd.DataFrame)
        self.assertIsInstance(x.by_category_aggreation_vs_overall["On-site Generation"], pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
