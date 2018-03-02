import unittest
from . bits import Bits

class TestBits(unittest.TestCase):
    def testCreateFromString(self):
        self.assertBits(Bits("0101"), "0101")

    def testCreateFromHex(self):
        self.assertBits(Bits.fromHex("00"), "0000 0000")
        self.assertBits(Bits.fromHex(""), "")
        self.assertBits(Bits.fromHex("123"), "0001 0010 0011")
        self.assertBits(Bits.fromHex("1BF"), "0001 1011 1111")

    def testCreateFromNumber(self):
        self.assertBits(Bits.fromPosInt(0, length = 5), "00000")
        self.assertBits(Bits.fromPosInt(12, length = 4), "1100")
        self.assertBits(Bits.fromPosInt(12, length = 6), "001100")

        with self.assertRaises(Exception):
            Bits.fromPosInt(16, length = 4)

    def testToInt(self):
        self.assertEqual(int(Bits.fromPosInt(12)), 12)
        self.assertEqual(int(Bits.fromPosInt(54)), 54)

    def assertBits(self, bits, string):
        self.assertEqual(bits, string.replace(" ", ""))

if __name__ == "__main__":
    unittest.main()
