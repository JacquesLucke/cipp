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
        self.assertBits(Bits.fromInt(0, length = 5), "00000")
        self.assertBits(Bits.fromInt(12, length = 4), "1100")
        self.assertBits(Bits.fromInt(12, length = 6), "001100")
        self.assertBits(Bits.fromInt(-1, length = 6), "111111")
        self.assertBits(Bits.fromInt(-42, length = 8), "11010110")

        with self.assertRaises(Exception):
            Bits.fromInt(16, length = 4)

    def testToInt(self):
        self.assertEqual(int(Bits.fromInt(12)), 12)
        self.assertEqual(int(Bits.fromInt(54)), 54)

    def testReversedBytes(self):
        self.assertEqual(Bits.fromHex("ABCDEF").reversedBytes(), Bits.fromHex("EFCDAB"))

    def assertBits(self, bits, string):
        self.assertEqual(bits, string.replace(" ", ""))

    def testToHex(self):
        self.assertEqual(Bits.fromHex("03CDF").toHex(), "03CDF")
        self.assertEqual(Bits.fromHex("").toHex(), "")

    def testToCArrayInitializer(self):
        self.assertEqual(Bits.fromHex("123456").toCArrayInitializer(), "{0x12, 0x34, 0x56}")

        with self.assertRaises(Exception):
            Bits.fromHex("123").toCArrayInitializer()

if __name__ == "__main__":
    unittest.main()
