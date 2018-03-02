'''
Online conversion: intel syntax -> binary:
    https://defuse.ca/online-x86-assembler.htm
'''

import unittest

from . instructions import PushInstr, PopInstr, RetInstr, AddRegToRegInstr, MovRegToRegInstr
from . registers import Registers
from . bits import Bits

eax = Registers.eax
ebx = Registers.ebx
ecx = Registers.ecx
edx = Registers.edx

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
