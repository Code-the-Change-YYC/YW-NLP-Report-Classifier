import unittest
import os

from incident_types import processor
from incident_types.incident_types_d import IncidentType, replacements
from report_data import ReportData

# use for filepath relative from this file
dir_path = os.path.dirname(os.path.realpath(__file__))

class TestIncTypeMapper(unittest.TestCase):
    def test_maps(self):
        """Ensure replacements are made as expected."""

        in_file_path = os.path.join(dir_path, '../../../preprocess/data/data-sensitive.csv')
        report_df = ReportData(in_file_path=in_file_path).get_raw_report_data()
        processor.IncidentTypesProcessor().process(report_df)
        for col_name in processor.IncTypeMapper.col_names:
            for inc_type in report_df[col_name].fillna(''):
                self.assertNotIn(inc_type, replacements.keys())
                self.assertIn(inc_type, [v.value for v in IncidentType.__members__.values()] + [''])


if __name__ == '__main__':
    unittest.main()
