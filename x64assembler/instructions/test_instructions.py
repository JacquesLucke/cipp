'''
Online conversion: intel syntax -> binary:
    https://defuse.ca/online-x86-assembler.htm
'''

import unittest

from .. bits import Bits
from .. registers import allRegisters
from . mov_reg_to_reg import MovRegToRegInstr
from . mov_imm_to_reg import MovImmToRegInstr
from . mov_mem_to_reg import MovMemToRegInstr
from . mov_reg_to_mem import MovRegToMemInstr
from . add_imm_to_reg import AddImmToRegInstr
from . add_reg_to_reg import AddRegToRegInstr
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
                arguments, machineCode, intelSyntax = case
                instruction = cls.instruction(*arguments)
                self.assertMachineCode(instruction, machineCode, intelSyntax)
                self.assertIntelSyntax(instruction, intelSyntax)
            testName = f"test{cls.__name__[4:]}_{i}"
            setattr(cls, testName, testSimpleCase)


class TestMovRegToRegInstruction(TestInstruction):
    instruction = MovRegToRegInstr
    simpleTestCases = [
        # 64 bit
        ([rax, rbx], "4889d8", "mov rax, rbx"),
        ([rsp, rax], "4889c4", "mov rsp, rax"),
        ([r12, r13], "4d89ec", "mov r12, r13"),
        ([r15, r8], "4d89c7", "mov r15, r8"),
        ([rax, r9], "4c89c8", "mov rax, r9"),
        ([rsp, r10], "4c89d4", "mov rsp, r10"),
        ([r14, rax], "4989c6", "mov r14, rax"),
        ([r12, rbx], "4989dc", "mov r12, rbx"),
        ([r8, r11], "4d89d8", "mov r8, r11"),

        # 32 bit
        ([eax, ebx], "89d8", "mov eax, ebx"),
        ([esp, edx], "89d4", "mov esp, edx"),
        ([r12d, r13d], "4589ec", "mov r12d, r13d"),
        ([r8d, r15d], "4589f8", "mov r8d, r15d"),
        ([eax, r10d], "4489d0", "mov eax, r10d"),
        ([ebx, r13d], "4489eb", "mov ebx, r13d"),
        ([r10d, edx], "4189d2", "mov r10d, edx"),
        ([r11d, ebp], "4189eb", "mov r11d, ebp"),

        # 16 bit
        ([ax, bx], "6689d8", "mov ax, bx"),
        ([sp, dx], "6689d4", "mov sp, dx"),
        ([r12w, r13w], "664589ec", "mov r12w, r13w"),
        ([r8w, r15w], "664589f8", "mov r8w, r15w"),
        ([ax, r10w], "664489d0", "mov ax, r10w"),
        ([bx, r13w], "664489eb", "mov bx, r13w"),
        ([r10w, dx], "664189d2", "mov r10w, dx"),
        ([r11w, bp], "664189eb", "mov r11w, bp")
    ]

    def testDisallowDifferentSizes(self):
        with self.assertRaises(Exception):
            MovRegToRegInstr(eax, rbx)
        with self.assertRaises(Exception):
            MovRegToRegInstr(r14, sp)

class TestAddImmToRegInstruction(TestInstruction):
    instruction = AddImmToRegInstr
    simpleTestCases = [
        # 64 bit
        ([rax, 10], "4883c00a", "add rax, 10"),
        ([r8, 10], "4983c00a", "add r8, 10"),
        ([rbx, -12], "4883c3f4", "add rbx, -12"),
        ([r9, -12], "4983c1f4", "add r9, -12"),
        ([rcx, 1000], "4881c1e8030000", "add rcx, 1000"),
        ([rbx, -1200], "4881c350fbffff", "add rbx, -1200"),
        ([r9, 1000], "4981c1e8030000", "add r9, 1000"),
        ([r11, -1200], "4981c350fbffff", "add r11, -1200"),
        ([rsp, 123456], "4881c440e20100", "add rsp, 123456"),
        ([rax, 1000], "4805e8030000", "add rax, 1000"),

        # 32 bit
        ([ecx, 10], "83c10a", "add ecx, 10"),
        ([ebx, -12], "83c3f4", "add ebx, -12"),
        ([r9d, 10], "4183c10a", "add r9d, 10"),
        ([r11d, -12], "4183c3f4", "add r11d, -12"),
        ([eax, 10], "83c00a", "add eax, 10"),
        ([ecx, 1000], "81c1e8030000", "add ecx, 1000"),
        ([ebx, -1200], "81c350fbffff", "add ebx, -1200"),
        ([r9d, 1000], "4181c1e8030000", "add r9d, 1000"),
        ([r11d, -1200], "4181c350fbffff", "add r11d, -1200"),
        ([eax, 1000], "05e8030000", "add eax, 1000"),

        # 16 bit
        ([cx, 10], "6683c10a", "add cx, 10"),
        ([bx, -12], "6683c3f4", "add bx, -12"),
        ([r9w, 10], "664183c10a", "add r9w, 10"),
        ([r11w, -12], "664183c3f4", "add r11w, -12"),
        ([ax, 10], "6683c00a", "add ax, 10"),
        ([cx, 1000], "6681c1e803", "add cx, 1000"),
        ([bx, -1200], "6681c350fb", "add bx, -1200"),
        ([r9w, 1000], "664181c1e803", "add r9w, 1000"),
        ([r11w, -1200], "664181c350fb", "add r11w, -1200"),
        ([ax, 1000], "6605e803", "add ax, 1000")
    ]

class TestRetnInstruction(TestInstruction):
    instruction = RetInstr
    simpleTestCases = [
        ([], "c3", "ret"),
        ([1234], "c2d204", "ret 1234"),
        ([8], "c20800", "ret 8")
    ]

class TestSyscallInstruction(TestInstruction):
    instruction = SyscallInstr
    simpleTestCases = [
        ([], "0f05", "syscall")
    ]

class TestPushRegInstruction(TestInstruction):
    instruction = PushRegInstr
    simpleTestCases = [
        # 64 bit
        ([rax], "50", "push rax"),
        ([rsp], "54", "push rsp"),
        ([r8], "4150", "push r8"),
        ([r15], "4157", "push r15"),

        # 16 bit
        ([bx], "6653", "push bx"),
        ([bp], "6655", "push bp"),
        ([r10w], "664152", "push r10w"),
        ([r12w], "664154", "push r12w")
    ]

class TestPopRegInstruction(TestInstruction):
    instruction = PopRegInstr
    simpleTestCases = [
        # 64 bit
        ([rax], "58", "pop rax"),
        ([rsp], "5c", "pop rsp"),
        ([r8], "4158", "pop r8"),
        ([r15], "415f", "pop r15"),

        # 16 bit
        ([bx], "665b", "pop bx"),
        ([bp], "665d", "pop bp"),
        ([r10w], "66415a", "pop r10w"),
        ([r12w], "66415c", "pop r12w")
    ]

class TestMovImmToRegInstruction(TestInstruction):
    instruction = MovImmToRegInstr
    simpleTestCases = [
        ([rax, 20], "48c7c014000000", "mov rax, 20"),
        ([rbp, 40], "48c7c528000000", "mov rbp, 40"),
        ([rsp, 1234567], "48c7c487d61200", "mov rsp, 1234567"),
        ([r8, 20], "49c7c014000000", "mov r8, 20"),
        ([r14, 42], "49c7c62a000000", "mov r14, 42"),
        ([rbx, 1345678900], "48C7C3346E3550", "mov rbx, 1345678900"),
        ([rdx, 98765432111], "48ba2fe5e0fe16000000", "mov rdx, 98765432111"),
        ([r8, -1234567890000], "49b8b0fb048ee0feffff", "mov r8, -1234567890000"),
        ([r12, 12345678900000000001], "49bc010889a18ca954ab", "mov r12, 12345678900000000001")
    ]

class TestPushImmInstruction(TestInstruction):
    instruction = PushImmInstr
    simpleTestCases = [
        ([10], "6a0a", "push 10"),
        ([-12], "6af4", "push -12"),
        ([550], "6826020000", "push 550"),
        ([-4600], "6808eeffff", "push -4600"),
        ([12345678], "684e61bc00", "push 12345678"),
        ([987654321], "68b168de3a", "push 987654321")
    ]

class TestMovMemToRegInstruction(TestInstruction):
    instruction = MovMemToRegInstr
    simpleTestCases = [
        ([rax, rax], "488b00", "mov rax, [rax]"),
        ([rbx, rdx], "488b1a", "mov rbx, [rdx]"),
        ([r8, r8], "4d8b00", "mov r8, [r8]"),
        ([r12, r15], "4d8b27", "mov r12, [r15]"),
        ([r10, rax], "4c8b10", "mov r10, [rax]"),
        ([r11, rbx], "4c8b1b", "mov r11, [rbx]"),
        ([rax, r11], "498b03", "mov rax, [r11]"),

        ([rax, rsp], "488b0424", "mov rax, [rsp]"),
        ([rax, rbp], "488b4500", "mov rax, [rbp]"),
        ([rbx, r13], "498b5d00", "mov rbx, [r13]"),
        ([rdx, r12], "498b1424", "mov rdx, [r12]")
    ]

class TestMovRegToMemInstruction(TestInstruction):
    instruction = MovRegToMemInstr
    simpleTestCases = [
        ([rax, rax], "488900", "mov [rax], rax"),
        ([rbx, rdx], "488913", "mov [rbx], rdx"),
        ([r15, r9], "4d890f", "mov [r15], r9"),
        ([rax, r10], "4c8910", "mov [rax], r10"),
        ([r14, rsp], "498926", "mov [r14], rsp"),
        ([r14, rax], "498906", "mov [r14], rax"),

        ([rsp, rax], "48890424", "mov [rsp], rax"),
        ([rbp, rcx], "48894d00", "mov [rbp], rcx"),
        ([r12, r8], "4d890424", "mov [r12], r8"),

        ([rsp, rax, 10], "488944240a", "mov [rsp+10], rax"),
        ([rdx, rcx, 100], "48894a64", "mov [rdx+100], rcx"),
        ([rdx, rcx, 1000], "48898ae8030000", "mov [rdx+1000], rcx"),
        ([rsp, r15, -1000], "4c89bc2418fcffff", "mov [rsp-1000], r15"),
        ([r14, r9, -16], "4d894ef0", "mov [r14-16], r9")
    ]

class TestAddRegToRegInstruction(TestInstruction):
    instruction = AddRegToRegInstr
    simpleTestCases = [
        # 64 bit
        ([rax, rax], "4801c0", "add rax, rax"),
        ([rdx, rsp], "4801e2", "add rdx, rsp"),
        ([r13, r15], "4d01fd", "add r13, r15"),
        ([r8, r10], "4d01d0", "add r8, r10"),
        ([rbx, r13], "4c01eb", "add rbx, r13"),
        ([rdi, r14], "4c01f7", "add rdi, r14"),
        ([r9, rbp], "4901e9", "add r9, rbp"),
        ([r11, rsp], "4901e3", "add r11, rsp"),

        # 32 bit
        ([eax, eax], "01c0", "add eax, eax"),
        ([edx, esp], "01e2", "add edx, esp"),
        ([r13d, r15d], "4501fd", "add r13d, r15d"),
        ([r8d, r10d], "4501d0", "add r8d, r10d"),
        ([ebx, r13d], "4401eb", "add ebx, r13d"),
        ([edi, r14d], "4401f7", "add edi, r14d"),
        ([r9d, ebp], "4101e9", "add r9d, ebp"),
        ([r11d, esp], "4101e3", "add r11d, esp"),

        # 16 bit
        ([ax, ax], "6601c0", "add ax, ax"),
        ([dx, sp], "6601e2", "add dx, sp"),
        ([r13w, r15w], "664501fd", "add r13w, r15w"),
        ([r8w, r10w], "664501d0", "add r8w, r10w"),
        ([bx, r13w], "664401eb", "add bx, r13w"),
        ([di, r14w], "664401f7", "add di, r14w"),
        ([r9w, bp], "664101e9", "add r9w, bp"),
        ([r11w, sp], "664101e3", "add r11w, sp")
    ]