import unittest

from incident_types import processor
import report_data


class TestIncTypes(unittest.TestCase):
    # TODO: Test that only incident types from the current dropdown are in the columns after pre-processing
    def test_preprocess(self):
        """Ensure replacements are made as expected"""
        report_df = report_data.get_raw_report_data()
        processor.IncidentTypesProcessor().process(report_df)
        for col_name in processor.IncidentTypesProcessor.col_names:
            for inc_type in report_df[col_name]:
                if inc_type in processor._t_replace_dict.keys():
                    self.fail()


if __name__ == '__main__':
    unittest.main()
