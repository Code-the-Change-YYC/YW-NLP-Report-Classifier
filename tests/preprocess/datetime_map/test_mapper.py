import unittest
from datetime import datetime

from datetime_map.mapper import DatetimeMapper
from report_data import ReportData
from report_data_d import _ColName


class TestDatetimeMapper(unittest.TestCase):
    dt_mapper = DatetimeMapper()
    report_data = ReportData(in_file_path='../../../preprocess/data/data-sensitive.csv').get_raw_report_data()

    def test_process_hour_of_day(self):
        report_data = self.dt_mapper.process(self.report_data)
        for hour in report_data[_ColName.HOUR_OF_DAY]:
            self.assertIsInstance(hour, int)
            self.assertIn(hour, range(0, 24))

    def test_process_weekday(self):
        report_data = self.dt_mapper.process(self.report_data)
        for is_weekday in report_data[_ColName.WEEKDAY]:
            self.assertIsInstance(is_weekday, int)
            self.assertTrue(is_weekday == 0 or is_weekday == 1)

    def test_process_time_of_day(self):
        report_data = self.dt_mapper.process(self.report_data)
        for col in _ColName.MORNING, _ColName.AFTERNOON, _ColName.EVENING, _ColName.NIGHT:
            for cell in report_data[col]:
                self.assertIsInstance(cell, int)
                self.assertTrue(cell == 0 or cell == 1)

    def test_parse_datetime(self):
        parsed = self.dt_mapper._parse_datetime('2019-02-05 18:10:00')
        expected = datetime(2019, 2, 5, 18, 10, 0)
        self.assertEqual(expected, parsed)
        parsed = self.dt_mapper._parse_datetime('2020-05-02 09:30:00')
        expected = datetime(2020, 5, 2, 9, 30, 0)
        self.assertEqual(expected, parsed)


if __name__ == '__main__':
    unittest.main()
