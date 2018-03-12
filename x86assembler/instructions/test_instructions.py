'''
Online conversion: intel syntax -> binary:
    https://defuse.ca/online-x86-assembler.htm
'''

import unittest

from .. bits import Bits
from .. registers import allRegisters
from . mov_reg_to_reg import MovRegToRegInstr
from . mov_imm_to_reg import MovImmToRegInstr
from . add_imm_to_reg import AddImmToRegInstr
from . push_imm import PushImmInstr
from . push_reg import PushRegInstr
from . syscall import SyscallInstr
from . pop_reg import PopRegInstr
from . ret import RetInstr

globals().update(allRegisters)

class TestInstruction(unittest.TestCase):
    simpleTestCases = []

    def assertMachineCode(self, instruction, expectedHex, message = None):
        generatedHex = instruction.toMachineCode().toHex()
        expectedHex = Bits.fromHex(expectedHex).toHex()
        self.assertEqual(generatedHex, expectedHex, message)

    def assertIntelSyntax(self, instruction, expected):
        self.assertEqual(instruction.toIntelSyntax(), expected)

    def __init_subclass__(cls):
        for i, case in enumerate(cls.simpleTestCases):
            def testSimpleCase(self, case = case):
                instruction, machineCode, intelSyntax = case
                self.assertMachineCode(instruction, machineCode, intelSyntax)
                self.assertIntelSyntax(instruction, intelSyntax)
            testName = f"test{cls.__name__[4:]}_{i}"
            setattr(cls, testName, testSimpleCase)


class TestMovRegToRegInstruction(TestInstruction):
    simpleTestCases = [
        # 64 bit
        (MovRegToRegInstr(rax, rbx), "4889d8", "mov rax, rbx"),
        (MovRegToRegInstr(rsp, rax), "4889c4", "mov rsp, rax"),
        (MovRegToRegInstr(r12, r13), "4d89ec", "mov r12, r13"),
        (MovRegToRegInstr(r15, r8), "4d89c7", "mov r15, r8"),
        (MovRegToRegInstr(rax, r9), "4c89c8", "mov rax, r9"),
        (MovRegToRegInstr(rsp, r10), "4c89d4", "mov rsp, r10"),
        (MovRegToRegInstr(r14, rax), "4989c6", "mov r14, rax"),
        (MovRegToRegInstr(r12, rbx), "4989dc", "mov r12, rbx"),
        (MovRegToRegInstr(r8, r11), "4d89d8", "mov r8, r11"),

        # 32 bit
        (MovRegToRegInstr(eax, ebx), "89d8", "mov eax, ebx"),
        (MovRegToRegInstr(esp, edx), "89d4", "mov esp, edx"),
        (MovRegToRegInstr(r12d, r13d), "4589ec", "mov r12d, r13d"),
        (MovRegToRegInstr(r8d, r15d), "4589f8", "mov r8d, r15d"),
        (MovRegToRegInstr(eax, r10d), "4489d0", "mov eax, r10d"),
        (MovRegToRegInstr(ebx, r13d), "4489eb", "mov ebx, r13d"),
        (MovRegToRegInstr(r10d, edx), "4189d2", "mov r10d, edx"),
        (MovRegToRegInstr(r11d, ebp), "4189eb", "mov r11d, ebp"),

        # 16 bit
        (MovRegToRegInstr(ax, bx), "6689d8", "mov ax, bx"),
        (MovRegToRegInstr(sp, dx), "6689d4", "mov sp, dx"),
        (MovRegToRegInstr(r12w, r13w), "664589ec", "mov r12w, r13w"),
        (MovRegToRegInstr(r8w, r15w), "664589f8", "mov r8w, r15w"),
        (MovRegToRegInstr(ax, r10w), "664489d0", "mov ax, r10w"),
        (MovRegToRegInstr(bx, r13w), "664489eb", "mov bx, r13w"),
        (MovRegToRegInstr(r10w, dx), "664189d2", "mov r10w, dx"),
        (MovRegToRegInstr(r11w, bp), "664189eb", "mov r11w, bp")
    ]

    def testDisallowDifferentSizes(self):
        with self.assertRaises(Exception):
            MovRegToRegInstr(eax, rbx)
        with self.assertRaises(Exception):
            MovRegToRegInstr(r14, sp)

class TestAddImmToRegInstruction(TestInstruction):
    simpleTestCases = [
        # 64 bit
        (AddImmToRegInstr(rax, 10), "4883c00a", "add rax, 10"),
        (AddImmToRegInstr(r8, 10), "4983c00a", "add r8, 10"),
        (AddImmToRegInstr(rbx, -12), "4883c3f4", "add rbx, -12"),
        (AddImmToRegInstr(r9, -12), "4983c1f4", "add r9, -12"),
        (AddImmToRegInstr(rcx, 1000), "4881c1e8030000", "add rcx, 1000"),
        (AddImmToRegInstr(rbx, -1200), "4881c350fbffff", "add rbx, -1200"),
        (AddImmToRegInstr(r9, 1000), "4981c1e8030000", "add r9, 1000"),
        (AddImmToRegInstr(r11, -1200), "4981c350fbffff", "add r11, -1200"),
        (AddImmToRegInstr(rsp, 123456), "4881c440e20100", "add rsp, 123456"),
        (AddImmToRegInstr(rax, 1000), "4805e8030000", "add rax, 1000"),

        # 32 bit
        (AddImmToRegInstr(ecx, 10), "83c10a", "add ecx, 10"),
        (AddImmToRegInstr(ebx, -12), "83c3f4", "add ebx, -12"),
        (AddImmToRegInstr(r9d, 10), "4183c10a", "add r9d, 10"),
        (AddImmToRegInstr(r11d, -12), "4183c3f4", "add r11d, -12"),
        (AddImmToRegInstr(eax, 10), "83c00a", "add eax, 10"),
        (AddImmToRegInstr(ecx, 1000), "81c1e8030000", "add ecx, 1000"),
        (AddImmToRegInstr(ebx, -1200), "81c350fbffff", "add ebx, -1200"),
        (AddImmToRegInstr(r9d, 1000), "4181c1e8030000", "add r9d, 1000"),
        (AddImmToRegInstr(r11d, -1200), "4181c350fbffff", "add r11d, -1200"),
        (AddImmToRegInstr(eax, 1000), "05e8030000", "add eax, 1000"),

        # 16 bit
        (AddImmToRegInstr(cx, 10), "6683c10a", "add cx, 10"),
        (AddImmToRegInstr(bx, -12), "6683c3f4", "add bx, -12"),
        (AddImmToRegInstr(r9w, 10), "664183c10a", "add r9w, 10"),
        (AddImmToRegInstr(r11w, -12), "664183c3f4", "add r11w, -12"),
        (AddImmToRegInstr(ax, 10), "6683c00a", "add ax, 10"),
        (AddImmToRegInstr(cx, 1000), "6681c1e803", "add cx, 1000"),
        (AddImmToRegInstr(bx, -1200), "6681c350fb", "add bx, -1200"),
        (AddImmToRegInstr(r9w, 1000), "664181c1e803", "add r9w, 1000"),
        (AddImmToRegInstr(r11w, -1200), "664181c350fb", "add r11w, -1200"),
        (AddImmToRegInstr(ax, 1000), "6605e803", "add ax, 1000")
    ]

class TestRetnInstruction(TestInstruction):
    simpleTestCases = [
        (RetInstr(), "c3", "ret"),
        (RetInstr(1234), "c2d204", "ret 1234"),
        (RetInstr(8), "c20800", "ret 8")
    ]

class TestSyscallInstruction(TestInstruction):
    simpleTestCases = [
        (SyscallInstr(), "0f05", "syscall")
    ]

class TestPushRegInstruction(TestInstruction):
    simpleTestCases = [
        # 64 bit
        (PushRegInstr(rax), "50", "push rax"),
        (PushRegInstr(rsp), "54", "push rsp"),
        (PushRegInstr(r8), "4150", "push r8"),
        (PushRegInstr(r15), "4157", "push r15"),

        # 16 bit
        (PushRegInstr(bx), "6653", "push bx"),
        (PushRegInstr(bp), "6655", "push bp"),
        (PushRegInstr(r10w), "664152", "push r10w"),
        (PushRegInstr(r12w), "664154", "push r12w")
    ]

class TestPopRegInstruction(TestInstruction):
    simpleTestCases = [
        # 64 bit
        (PopRegInstr(rax), "58", "pop rax"),
        (PopRegInstr(rsp), "5c", "pop rsp"),
        (PopRegInstr(r8), "4158", "pop r8"),
        (PopRegInstr(r15), "415f", "pop r15"),

        # 16 bit
        (PopRegInstr(bx), "665b", "pop bx"),
        (PopRegInstr(bp), "665d", "pop bp"),
        (PopRegInstr(r10w), "66415a", "pop r10w"),
        (PopRegInstr(r12w), "66415c", "pop r12w")
    ]

class TestMovImmToRegInstruction(TestInstruction):
    simpleTestCases = [
        (MovImmToRegInstr(rax, 20), "48c7c014000000", "mov rax, 20"),
        (MovImmToRegInstr(rbp, 40), "48c7c528000000", "mov rbp, 40"),
        (MovImmToRegInstr(rsp, 1234567), "48c7c487d61200", "mov rsp, 1234567"),
        (MovImmToRegInstr(r8, 20), "49c7c014000000", "mov r8, 20"),
        (MovImmToRegInstr(r14, 42), "49c7c62a000000", "mov r14, 42"),
        (MovImmToRegInstr(rbx, 1345678900), "48C7C3346E3550", "mov rbx, 1345678900"),
        (MovImmToRegInstr(rdx, 98765432111), "48ba2fe5e0fe16000000", "mov rdx, 98765432111"),
        (MovImmToRegInstr(r8, -1234567890000), "49b8b0fb048ee0feffff", "mov r8, -1234567890000"),
        (MovImmToRegInstr(r12, 12345678900000000001), "49bc010889a18ca954ab", "mov r12, 12345678900000000001")
    ]

class TestPushImmInstruction(TestInstruction):
    simpleTestCases = [
        (PushImmInstr(10), "6a0a", "push 10"),
        (PushImmInstr(-12), "6af4", "push -12"),
        (PushImmInstr(550), "6826020000", "push 550"),
        (PushImmInstr(-4600), "6808eeffff", "push -4600"),
        (PushImmInstr(12345678), "684e61bc00", "push 12345678"),
        (PushImmInstr(987654321), "68b168de3a", "push 987654321")
    ]
