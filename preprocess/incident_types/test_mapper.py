import unittest

from incident_types import processor
from incident_types.incident_types_d import IncidentType, replacements
from report_data import ReportData


class TestIncTypeMapper(unittest.TestCase):
    def test_maps(self):
        """Ensure replacements are made as expected."""
        report_df = ReportData().get_raw_report_data()
        processor.IncidentTypesProcessor().process(report_df)
        for col_name in processor.IncTypeMapper.col_names:
            for inc_type in report_df[col_name].fillna(''):
                self.assertNotIn(inc_type, replacements.keys())
                self.assertIn(inc_type, [v.value for v in IncidentType.__members__.values()] + [''])


if __name__ == '__main__':
    unittest.main()
