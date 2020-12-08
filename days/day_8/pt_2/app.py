"""
--- Day 8: Handheld Halting ---
Your flight to the major airline hub reaches cruising altitude without incident.
While you consider checking the in-flight menu for one of those drinks that come with a little
umbrella, you are interrupted by the kid sitting next to you.

Their handheld game console won't turn on! They ask if you can take a look.

You narrow the problem down to a strange infinite loop in the boot code (your puzzle input)
of the device.
You should be able to fix it, but first you need to be able to run the code in isolation.

The boot code is represented as a text file with one instruction per line of text.
Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed
number like +4 or -20).

acc increases or decreases a single global value called the accumulator by the value given in the argument.

```
acc +7 would increase the accumulator by 7.
    The accumulator starts at 0.
    After an acc instruction, the instruction immediately below it is executed next.

jmp jumps to a new instruction relative to itself.
    The next instruction to execute is found using the argument as an offset from the jmp instruction;
    for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction
    immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.

nop stands for No OPeration - it does nothing.
    The instruction immediately below it is executed next.
```

For example, consider the following program:

```
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
```

These instructions are visited in this order:

```
nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |
```

First, the nop +0 does nothing.
Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to
the other acc +1 near the bottom.
After it increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction
to the only acc +3.
It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.

This is an infinite loop: with this sequence of jumps, the program will run forever.
The moment the program tries to run any instruction a second time, you know it will never terminate.

Immediately before the program would run an instruction a second time, the value in the accumulator is 5.

Run your copy of the boot code.
Immediately before any instruction is executed a second time, what value is in the accumulator?


--- Part Two ---
After some careful analysis, you believe that exactly one instruction is corrupted.

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp.
(No acc instructions were harmed in the corruption of this boot code.)

The program is supposed to terminate by attempting to execute an instruction immediately after the last
instruction in the file.
By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

For example, consider the same program from above:

```
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
```

If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop,
never leaving that instruction.
If you change almost any of the jmp instructions, the program will still eventually find another
jmp instruction and loop forever.

However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates!
The instructions are visited in this order:

```
nop +0  | 1
acc +1  | 2
jmp +4  | 3
acc +3  |
jmp -3  |
acc -99 |
acc +1  | 4
nop -4  | 5
acc +6  | 6
```

After the last instruction (acc +6), the program terminates by attempting to run the instruction below the
last instruction in the file.
With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp).
What is the value of the accumulator after the program terminates?
"""
from collections import deque, Counter
from dataclasses import dataclass
from enum import Enum
import re
from typing import List


class InstructionEnum(str, Enum):
    acc = "acc"
    jmp = "jmp"
    nop = "nop"


@dataclass
class Instruction:
    name: InstructionEnum
    value: int


class VM:

    def __init__(self, instructions: List[Instruction], max_iteration: int = 2):
        self._max_iterations = max_iteration
        self._acc = 0

        self._instructions = instructions
        self._current_idx = 0

        self._instruction_counter = Counter()

        self._instructions_map = {
            InstructionEnum.acc: self.update_acc,
            InstructionEnum.jmp: self.jump,
            InstructionEnum.nop: self.nop
        }

    def __repr__(self):
        return f"VM(acc={self._acc}, idx={self._current_idx})"

    def run(self):

        while True:
            self.update_counter(self._current_idx)

            try:
                current_instruction = self._instructions[self._current_idx]
            except IndexError:
                return self._acc
            else:
                f = self._instructions_map[current_instruction.name]
                f(value=current_instruction.value)

    def update_counter(self, idx):
        self._instruction_counter[idx] += 1
        if self._instruction_counter[idx] == self._max_iterations:
            raise StopIteration(f"VM has reached max iterations. Current ACC: {self._acc}")

    def jump(self, value: int):
        self._current_idx += value

    def update_acc(self, value: int):
        self._acc += value
        self.jump(1)

    def nop(self, value: int):
        self.jump(value=1)


def create_instructions(lines: List[str]):
    instruction_ptrn = re.compile(r"^(?P<name>\w+)\s(?P<value>.*)$")

    instructions = []

    for idx, line in enumerate(lines):
        m = instruction_ptrn.match(line)
        instructions.append(Instruction(
            name=InstructionEnum(m.group("name")),
            value=int(m.group("value"))
        ))

    return instructions


def main(input_):

    instructions = create_instructions(input_.splitlines())

    for idx in range(len(instructions)):
        original_instruction = instructions[idx]

        if original_instruction.name != InstructionEnum.acc:
            print(original_instruction)

            name = InstructionEnum.jmp if original_instruction.name == InstructionEnum.nop else InstructionEnum.nop
            instructions[idx] = Instruction(name=name, value=original_instruction.value)

            vm = VM(instructions=instructions)

            try:
                print(vm.run())
                return

            except StopIteration:
                instructions[idx] = original_instruction


if __name__ == '__main__':
    main("""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""")
