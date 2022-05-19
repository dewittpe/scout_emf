import scout
import unittest
import pandas as pd
import gzip
import tempfile
import os
import json

class TestUtilities(unittest.TestCase):

    def test_import_baseline(self):

        with gzip.open("./supporting_data/stock_energy_tech_data/mseg_res_com_emm.gz", 'r') as f:
            file_content = f.read()

        json_str = file_content.decode("utf-8")

        bldg_metadata, baseline_data = scout.baseline.import_baseline(json.loads(file_content))

        self.assertIsInstance(bldg_metadata, pd.DataFrame)
        self.assertIsInstance(baseline_data, pd.DataFrame)



if __name__ == "__main__":
    unittest.main()
