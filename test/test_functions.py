import unittest

from utils.helpers import filter_bad_requests, csv_to_dict


class FunctionsTest(unittest.TestCase):

    def test_filter_bad_nodes(self):
        # we must to have a local elasticsearch connection
        nodes = ["http://localhost:9200", "http://badhost:9200"]
        expected = ["http://localhost:9200"]
        result = filter_bad_requests(nodes)
        self.assertEqual(expected, result)

    def test_csv_to_dict(self):
        csv = '"TagId";"TagName";"Value";"AlStatus";"AlType";"Quality"\r\n' \
                  '2;"VF1_Bus_CC";403.047;0;0;65472\r\n' \
                  '3;"VF1_FS_HZ";0;0;0;65472'
        expected = {'VF1_Bus_CC': '403.047', 'VF1_FS_HZ': '0'}
        result = csv_to_dict(csv)
        print(result)
        self.assertEqual(expected, result)
