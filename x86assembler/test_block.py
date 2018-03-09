import unittest

from . bits import Bits
from . block import Block
from . instructions import PushRegInstr, RetInstr, AddImmToRegInstr
from . registers import allRegisters

globals().update(allRegisters)

class TestBlock(unittest.TestCase):
    def testToIntelSyntax(self):
        instructions = [
            PushRegInstr(rax),
            AddImmToRegInstr(ecx, 10),
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
            PushRegInstr(rbx),
            AddImmToRegInstr(eax, 12)
        ]
        machineCode = Bits.join(
            instructions[0].toMachineCode(),
            instructions[1].toMachineCode(),
            instructions[2].toMachineCode()
        )
        block = Block(instructions)
        self.assertEqual(block.toMachineCode(), machineCode)
