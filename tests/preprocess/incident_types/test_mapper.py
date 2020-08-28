import unittest

from incident_types.column_merge import ColumnMerger
from incident_types.incident_types_d import IncidentType, replacements
from incident_types.mapper import IncTypeMapper
from incident_types.processor import IncidentTypesProcessor
from report_data import ReportData
from report_data_d import _ColName


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

    def test_preserves_new_secondary_types(self):
        """
        Context:

        Secondary incidents of type 'Other' have an optional text input
        for a more specific description. These values account for the
        `ColName.INC_T2_OLD` column.

        Test:

        Ensure text inputs are used instead of 'Other' when possible for
        secondary incident type.
        """

        report_df = ReportData().get_raw_report_data()
        rows = (report_df[_ColName.INC_T2] == IncidentType.OTR.value) & (report_df[_ColName.INC_T2_OLD].notnull())
        text_inputs = report_df[rows][_ColName.INC_T2_OLD]
        ColumnMerger().process(report_df)
        for val, text_input in zip(report_df[rows][_ColName.INC_T2], text_inputs):
            self.assertNotEqual(val, IncidentType.OTR.value)
            self.assertEqual(val, text_input)


if __name__ == '__main__':
    unittest.main()
