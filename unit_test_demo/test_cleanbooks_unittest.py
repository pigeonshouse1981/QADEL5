import sys
import os
import unittest
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cleanbooks import (
    clean_quotes,
    parse_dates,
    drop_all_na,
    fill_nans,
    fix_negative_days,
    process_csv
)

class TestCleanBooks(unittest.TestCase):

    def setUp(self):
        self.file_path = r"C:\Users\Admin\Desktop\QADEL5\data\03_Library Systembook.csv"
     

    def test_process_csv_runs(self):

        df = process_csv(self.file_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('Days Between', df.columns)
        self.assertFalse(df['Days Between'].isna().any(), "Some Days Between values are NaN")
        self.assertTrue((df['Days Between'] >= 0).all(), "Some Days Between values are negative")   

    def test_parse_dates(self):
        df = process_csv(self.file_path)
        df = clean_quotes(df, 'Book checkout')
        df = parse_dates(df, ['Book checkout', 'Book Returned'])
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['Book checkout']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['Book Returned']))

    


if __name__ == '__main__':
    unittest.main()
