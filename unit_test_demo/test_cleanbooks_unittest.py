git add .
git commit -m "Removed ipynbs"
git pushimport unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from cleanbooks import (
    clean_quotes,
    parse_dates,
    drop_all_na,
    fill_nans,
    fix_negative_days
)

class TestCleanBooks(unittest.TestCase):

    def setUp(self):
        self.file_path = r"C:\Users\Admin\Desktop\QADEL5\data\03_Library Systembook.csv"
     

    def test_process_csv_runs(self):

        df = process_csv(self.file_path)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('Days Between', df.columns)
        self.assertTrue((df['Days Between'] >= 0).all()) 
    


if __name__ == '__main__':
    unittest.main()
