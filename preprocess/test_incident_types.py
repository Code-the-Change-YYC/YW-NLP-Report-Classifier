import unittest

import incident_types
import report_data


class TestIncTypes(unittest.TestCase):
    # TODO: Test that only incident types from the current dropdown are in the columns after pre-processing
    def test_preprocess(self):
        """Ensure replacements are made as expected"""
        report_df = report_data.get_raw_report_data()
        incident_types.IncidentTypesProcessor().process(report_df)
        for col_name in incident_types.IncidentTypesProcessor.col_names:
            for inc_type in report_df[col_name]:
                if inc_type in incident_types._t_replace_dict.keys():
                    self.fail()


if __name__ == '__main__':
    unittest.main()
