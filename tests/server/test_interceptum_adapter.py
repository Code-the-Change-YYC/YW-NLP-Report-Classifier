from unittest import TestCase, main
from server.interceptum_adapter import InterceptumAdapter


with open('tests/server/interceptum-response.xml', 'r') as xml_file:
    xml = xml_file.read()


class TestXmlToFormValues(TestCase):
    def test_mapping(self):
        result = InterceptumAdapter.xml_to_form_values(xml)
        expected = {}
        self.assertDictEqual(result, expected)


if __name__ == '__main__':
    main()
