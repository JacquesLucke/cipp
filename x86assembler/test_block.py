import unittest

from . bits import Bits
from . block import Block
'''
from . instructions import PushInstr, RetInstr, AddRegToRegInstr
from . registers import eax, ebx, ecx, edx

class TestBlock(unittest.TestCase):
    def testToIntelSyntax(self):
        instructions = [
            PushInstr(eax),
            AddRegToRegInstr(ecx, ebx),
            RetInstr()
        ]
        intelSyntax = "\n".join((
            instructions[0].toIntelSyntax(),
            instructions[1].toIntelSyntax(),
            instructions[2].toIntelSyntax()
        ))
        block = Block(instructions)
        self.assertEqual(block.toIntelSyntax(), intelSyntax)

    def testToMachineCode(self):
        instructions = [
            RetInstr(),
            PushInstr(ebx),
            AddRegToRegInstr(eax, edx)
        ]
        machineCode = Bits.join(
            instructions[0].toMachineCode(),
            instructions[1].toMachineCode(),
            instructions[2].toMachineCode()
        )
        block = Block(instructions)
        self.assertEqual(block.toMachineCode(), machineCode)
'''
