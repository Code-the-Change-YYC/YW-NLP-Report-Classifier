import unittest

import pandas as pd

from scrubber import incident_types


class TestIncTypes(unittest.TestCase):
    # TODO: Test that only incident types from the current dropdown are in the columns after pre-processing
    def test_preprocess(self):
        """Ensure replacements are made as expected"""
        # TODO: Extract data loading and allow for the removal of specific steps
        # so we can test them
        report_data = pd.read_csv("data_scrubbed.csv")
        incident_types.preprocess(report_data)
        for col_name in incident_types.inc_type_col_names:
            for inc_type in report_data[col_name]:
                if inc_type in incident_types._t_replace_dict.keys():
                    self.fail()


if __name__ == '__main__':
    unittest.main()
