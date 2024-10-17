import unittest
import re
import time
from uuid_v9 import uuidv9, validate_uuidv9, verify_checksum

uuid_regex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
uuid_v1_regex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.I)
uuid_v4_regex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.I)
uuid_v9_regex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-9[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

class TestUUIDV9(unittest.TestCase):
    def test_validate_as_uuidv9(self):
        id1 = uuidv9()
        id2 = uuidv9('a1b2c3d4')
        id3 = uuidv9('', False)
        id4 = uuidv9('a1b2c3d4', False)
        self.assertTrue(uuid_regex.match(id1))
        self.assertTrue(uuid_regex.match(id2))
        self.assertTrue(uuid_regex.match(id3))
        self.assertTrue(uuid_regex.match(id4))

    def test_generate_sequential_ids(self):
        id1 = uuidv9()
        time.sleep(2)
        id2 = uuidv9()
        time.sleep(2)
        id3 = uuidv9()
        self.assertTrue(id1 < id2)
        self.assertTrue(id2 < id3)

    def test_generate_sequential_ids_with_prefix(self):
        id1 = uuidv9('a1b2c3d4')
        time.sleep(2)
        id2 = uuidv9('a1b2c3d4')
        time.sleep(2)
        id3 = uuidv9('a1b2c3d4')
        self.assertTrue(id1 < id2)
        self.assertTrue(id2 < id3)
        self.assertEqual(id1[:8], 'a1b2c3d4')
        self.assertEqual(id2[:8], 'a1b2c3d4')
        self.assertEqual(id3[:8], 'a1b2c3d4')
        self.assertEqual(id1[14:18], id2[14:18])
        self.assertEqual(id2[14:18], id3[14:18])

    def test_generate_non_sequential_ids(self):
        idS = uuidv9('', False)
        time.sleep(2)
        idNs = uuidv9('', False)
        self.assertNotEqual(idS[:4], idNs[:4])

    def test_generate_non_sequential_ids_with_prefix(self):
        idS = uuidv9('a1b2c3d4', False)
        time.sleep(2)
        idNs = uuidv9('a1b2c3d4', False)
        self.assertEqual(idS[:8], 'a1b2c3d4')
        self.assertEqual(idNs[:8], 'a1b2c3d4')
        self.assertNotEqual(idS[14:18], idNs[14:18])

    def test_generate_ids_with_checksum(self):
        id = uuidv9('', True, True)
        self.assertTrue(verify_checksum(id))
        self.assertTrue(uuid_regex.match(id))

    def test_generate_ids_with_version(self):
        id = uuidv9('', True, False, True)
        self.assertTrue(uuid_v9_regex.match(id))

    def test_generate_ids_with_compatibility(self):
        id1 = uuidv9('', True, False, False, True)
        id2 = uuidv9('a1b2c3d4', True, False, False, True)
        id3 = uuidv9('', False, False, False, True)
        id4 = uuidv9('a1b2c3d4', False, False, False, True)
        self.assertTrue(uuid_v1_regex.match(id1))
        self.assertTrue(uuid_v1_regex.match(id2))
        self.assertTrue(uuid_v4_regex.match(id3))
        self.assertTrue(uuid_v4_regex.match(id4))


    def test_validate_and_verify_checksum(self):
        id1 = uuidv9('', True, True)
        id2 = uuidv9('', False, True)
        id3 = uuidv9('a1b2c3d4', True, True)
        id4 = uuidv9('a1b2c3d4', False, True)
        id5 = uuidv9('', True, True, False, True)
        id6 = uuidv9('', False, True, True, True)
        self.assertTrue(validate_uuidv9(id1, True))
        self.assertTrue(validate_uuidv9(id2, True))
        self.assertTrue(validate_uuidv9(id3, True))
        self.assertTrue(validate_uuidv9(id4, True))
        self.assertTrue(validate_uuidv9(id5, True, '1'))
        self.assertTrue(validate_uuidv9(id6, True, '4'))
        self.assertTrue(verify_checksum(id1))
        self.assertTrue(verify_checksum(id2))
        self.assertTrue(verify_checksum(id3))
        self.assertTrue(verify_checksum(id4))
        self.assertTrue(verify_checksum(id5))
        self.assertTrue(verify_checksum(id6))

if __name__ == '__main__':
    unittest.main()
