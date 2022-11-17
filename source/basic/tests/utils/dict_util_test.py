import unittest

from utils.dict_util import bytes_dict_to_str_dict


class TestDictUtil(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_bytes_dict_to_str_dict(self):
        byte_dict = {b'gpus': b'8'}
        check = {'gpus': 8}
        result = bytes_dict_to_str_dict(byte_dict)
        self.assertDictEqual(result, check)
