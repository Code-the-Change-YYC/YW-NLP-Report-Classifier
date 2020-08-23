import unittest

from report_data import ReportData
from report_data_d import _ColName
from spacy_scrubber.description_scrub import DescriptionScrubber


class TestDescriptionScrubber(unittest.TestCase):
    def test_process_without_uids_for_initial(self):
        report_data = ReportData().get_raw_report_data()
        processed = DescriptionScrubber(ent_replacement='someone').process(report_data)
        for desc in processed[_ColName.DESC]:
            self.assertNotIn('*', desc)


if __name__ == '__main__':
    unittest.main()
