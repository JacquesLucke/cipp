'''
Online conversion: intel syntax -> binary:
    https://defuse.ca/online-x86-assembler.htm
'''

import unittest

from . instructions import PushInstr, PopInstr, RetInstr, AddRegToRegInstr, MovRegToRegInstr, IncInstr, DecInstr, MovImmToRegInstr, MovMemOffsetToRegInstr
from . registers import eax, ebx, ecx, edx, esp
from . bits import Bits

class TestInstruction(unittest.TestCase):
    simpleTestCases = []

    def assertMachineCode(self, instruction, expectedHex, message = None):
        self.assertEqual(instruction.toMachineCode(), Bits.fromHex(expectedHex), message)

    def assertIntelSyntax(self, instruction, expected):
        self.assertEqual(instruction.toIntelSyntax(), expected)

    def __init_subclass__(cls):
        def testSimpleCases(self):
            for instruction, machineCode, intelSyntax in self.simpleTestCases:
                self.assertMachineCode(instruction, machineCode, intelSyntax)
                self.assertIntelSyntax(instruction, intelSyntax)
        testName = "test" + cls.__name__[4:]
        setattr(cls, testName, testSimpleCases)


class TestPushInstruction(TestInstruction):
    simpleTestCases = [
        (PushInstr(eax), "50", "push eax"),
        (PushInstr(ebx), "53", "push ebx")
    ]

class TestPopInstruction(TestInstruction):
    simpleTestCases = [
        (PopInstr(eax), "58", "pop eax"),
        (PopInstr(edx), "5A", "pop edx")
    ]

class TestRetInstruction(TestInstruction):
    simpleTestCases = [
        (RetInstr(), "C3", "ret")
    ]

class TestAddRegToRegInstruction(TestInstruction):
    simpleTestCases = [
        (AddRegToRegInstr(eax, edx), "01D0", "add eax, edx"),
        (AddRegToRegInstr(ecx, ecx), "01C9", "add ecx, ecx")
    ]

class TestMovRegToRegInstruction(TestInstruction):
    simpleTestCases = [
        (MovRegToRegInstr(ebx, edx), "89D3", "mov ebx, edx"),
        (MovRegToRegInstr(eax, ebx), "89D8", "mov eax, ebx")
    ]

class TestIncInstruction(TestInstruction):
    simpleTestCases = [
        (IncInstr(eax), "40", "inc eax"),
        (IncInstr(ebx), "43", "inc ebx")
    ]

class TestDecInstruction(TestInstruction):
    simpleTestCases = [
        (DecInstr(eax), "48", "dec eax"),
        (DecInstr(ebx), "4B", "dec ebx")
    ]

class TestMovImmToRegInstruction(TestInstruction):
    simpleTestCases = [
        (MovImmToRegInstr(eax, 0), "B800000000", "mov eax, 0"),
        (MovImmToRegInstr(ecx, 2049), "B901080000", "mov ecx, 2049")
    ]

class TestMovMemOffsetToRegInstr(TestInstruction):
    simpleTestCases = [
        (MovMemOffsetToRegInstr(eax, ebx, 100000), "8B83A0860100", "mov eax, [ebx + 100000]"),
        (MovMemOffsetToRegInstr(eax, ebx, -100000), "8B836079FEFF", "mov eax, [ebx - 100000]"),
        (MovMemOffsetToRegInstr(ecx, eax, 0), "8B08", "mov ecx, [eax]"),
        (MovMemOffsetToRegInstr(ecx, eax, 1000), "8B88E8030000", "mov ecx, [eax + 1000]"),
        (MovMemOffsetToRegInstr(eax, edx, 4), "8B4204", "mov eax, [edx + 4]"),
        #(MovMemOffsetToRegInstr(eax, esp, 0), "8B0424", "mov eax, [esp]")
    ]
