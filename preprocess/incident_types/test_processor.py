import unittest

import incident_types.incident_types_d
from incident_types import processor
from report_data import ReportData


class TestProcessor(unittest.TestCase):
    # TODO: Test that only incident types from the current dropdown are in the columns after pre-processing
    def test_process(self):
        """Ensure replacements are made as expected"""
        report_df = ReportData().get_raw_report_data()
        processor.IncidentTypesProcessor().process(report_df)
        for col_name in processor.IncidentTypesProcessor.col_names:
            for inc_type in report_df[col_name]:
                if inc_type in incident_types.incident_types_d.replacements.keys():
                    self.fail()


if __name__ == '__main__':
    unittest.main()
