import unittest

from incident_types.incident_types_d import IncidentType, replacements
from incident_types.mapper import IncTypeMapper
from incident_types.processor import IncidentTypesProcessor
from report_data import ReportData


class TestIncTypeMapper(unittest.TestCase):
    def test_maps(self):
        """Ensure replacements are made as expected."""

        report_df = ReportData().get_raw_report_data()
        IncidentTypesProcessor().process(report_df)
        replacements_keys = [IncTypeMapper.normalize_inc_type(key) for key in replacements.keys()]
        incident_type_values = [v.value for v in IncidentType] + ['']
        for col_name in IncTypeMapper.col_names:
            for inc_type in report_df[col_name].fillna(''):
                self.assertNotIn(inc_type, replacements_keys)
                self.assertIn(inc_type, incident_type_values)


if __name__ == '__main__':
    unittest.main()
