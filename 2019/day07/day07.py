############# py #############
"""
# IntCode

This is an interpreter for [Advent of Code](https://adventofcode.com/) 2019's IntCode.

IntCode was first introduced in [Day 2](https://adventofcode.com/2019/day/2). This first
iteration required **ADD**, **MULTIPLY**, and **HALT** commands.

IntCode was expanded in [Day 5](https://adventofcode.com/2019/day/5). In this iteration,
the concept of *parameter modes* was introduced, and six more instructions were added:
**INPUT**, **OUTPUT**, **JUMP-IF-TRUE**, **JUMP-IF-FALSE**, **LESS-THAN**, and **EQUALS**.
"""

import warnings


class IntCodeProgram:
    """
  An intcode program, represented as a list of values/instructions (memory) and
  an instruction pointer.
  """
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99

    OPCODES = (ADD, MUL, INPUT, OUTPUT, JUMP_IF_TRUE, JUMP_IF_FALSE, LESS_THAN,
               EQUALS, HALT)

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1

    def __init__(self, values, user_input=[]):
        self.memory = values.copy()
        self.instruction_pointer = 0
        self._user_input = user_input
        self.output = list()

    def set_noun(self, noun):
        """Sets the noun (memory value 1)"""
        self.memory[1] = noun

    def set_verb(self, verb):
        """Sets the verb (memory value 2)"""
        self.memory[2] = verb

    @classmethod
    def from_text(cls, text, user_input=[]):
        """
    Creates an IntCodeProgram from text.

    The given string should be a comma-separated list of integers.
    """
        return cls([int(n) for n in text.split(',')], user_input)

    @staticmethod
    def _get_modes(value, number_of_modes=3):
        modes = str(value // 100)
        modes_tuple = None
        if number_of_modes == 0:
            modes_tuple = ()

        elif number_of_modes == 1:
            modes_tuple = (int(modes[0]), )

        elif number_of_modes == 2:
            if len(modes) == 1:
                modes_tuple = (int(modes[0]), IntCodeProgram.POSITION_MODE)
            elif len(modes) == 2:
                modes_tuple = (int(modes[1]), int(modes[0]))

        elif number_of_modes == 3:
            if len(modes) == 1:
                modes_tuple = (int(modes[0]), IntCodeProgram.POSITION_MODE,
                               IntCodeProgram.POSITION_MODE)
            elif len(modes) == 2:
                modes_tuple = (int(modes[1]), int(modes[0]),
                               IntCodeProgram.POSITION_MODE)
            elif len(modes) == 3:
                modes_tuple = (int(modes[2]), int(modes[1]), int(modes[0]))

        else:
            raise Exception(f'Unrecognized number of modes {number_of_modes}')

        return modes_tuple

    def _add(self):
        modes = IntCodeProgram._get_modes(
            self.memory[self.instruction_pointer], number_of_modes=3)
        if modes[2] == IntCodeProgram.IMMEDIATE_MODE:
            raise Exception("Cannot write to an immediate mode value")

        value_a = self.memory[self.instruction_pointer + 1]
        if modes[0] == IntCodeProgram.POSITION_MODE:
            value_a = self.memory[value_a]

        value_b = self.memory[self.instruction_pointer + 2]
        if modes[1] == IntCodeProgram.POSITION_MODE:
            value_b = self.memory[value_b]

        destination = self.memory[self.instruction_pointer + 3]

        self.memory[destination] = value_a + value_b
        self.instruction_pointer += 4

    def _mul(self):
        modes = IntCodeProgram._get_modes(
            self.memory[self.instruction_pointer], number_of_modes=3)
        if modes[2] == IntCodeProgram.IMMEDIATE_MODE:
            raise Exception("Cannot write to an immediate mode value")

        value_a = self.memory[self.instruction_pointer + 1]
        if modes[0] == IntCodeProgram.POSITION_MODE:
            value_a = self.memory[value_a]

        value_b = self.memory[self.instruction_pointer + 2]
        if modes[1] == IntCodeProgram.POSITION_MODE:
            value_b = self.memory[value_b]

        destination = self.memory[self.instruction_pointer + 3]

        self.memory[destination] = value_a * value_b
        self.instruction_pointer += 4

    def _input(self):
        if len(self._user_input) == 0:
            return
        address = self.memory[self.instruction_pointer + 1]
        self.memory[address] = self._user_input.pop(0)

        self.instruction_pointer += 2

    def _output(self):
        modes = IntCodeProgram._get_modes(
            self.memory[self.instruction_pointer], number_of_modes=1)
        value_a = self.memory[self.instruction_pointer + 1]
        if modes[0] == IntCodeProgram.POSITION_MODE:
            value_a = self.memory[value_a]

        self.output.append(value_a)

        self.instruction_pointer += 2

    def _jump_if_true(self):
        modes = IntCodeProgram._get_modes(
            self.memory[self.instruction_pointer], number_of_modes=2)

        value_a = self.memory[self.instruction_pointer + 1]
        if modes[0] == IntCodeProgram.POSITION_MODE:
            value_a = self.memory[value_a]

        value_b = self.memory[self.instruction_pointer + 2]
        if modes[1] == IntCodeProgram.POSITION_MODE:
            value_b = self.memory[value_b]

        if value_a != 0:
            self.instruction_pointer = value_b
        else:
            self.instruction_pointer += 3

    def _jump_if_false(self):
        modes = IntCodeProgram._get_modes(
            self.memory[self.instruction_pointer], number_of_modes=2)

        value_a = self.memory[self.instruction_pointer + 1]
        if modes[0] == IntCodeProgram.POSITION_MODE:
            value_a = self.memory[value_a]

        value_b = self.memory[self.instruction_pointer + 2]
        if modes[1] == IntCodeProgram.POSITION_MODE:
            value_b = self.memory[value_b]

        if value_a == 0:
            self.instruction_pointer = value_b
        else:
            self.instruction_pointer += 3

    def _less_than(self):
        modes = IntCodeProgram._get_modes(
            self.memory[self.instruction_pointer], number_of_modes=3)
        if modes[2] == IntCodeProgram.IMMEDIATE_MODE:
            raise Exception("Cannot write to an immediate mode value")

        value_a = self.memory[self.instruction_pointer + 1]
        if modes[0] == IntCodeProgram.POSITION_MODE:
            value_a = self.memory[value_a]

        value_b = self.memory[self.instruction_pointer + 2]
        if modes[1] == IntCodeProgram.POSITION_MODE:
            value_b = self.memory[value_b]

        destination = self.memory[self.instruction_pointer + 3]

        if value_a < value_b:
            self.memory[destination] = 1
        else:
            self.memory[destination] = 0
        self.instruction_pointer += 4

    def _equals(self):
        modes = IntCodeProgram._get_modes(
            self.memory[self.instruction_pointer], number_of_modes=3)
        if modes[2] == IntCodeProgram.IMMEDIATE_MODE:
            raise Exception("Cannot write to an immediate mode value")

        value_a = self.memory[self.instruction_pointer + 1]
        if modes[0] == IntCodeProgram.POSITION_MODE:
            value_a = self.memory[value_a]

        value_b = self.memory[self.instruction_pointer + 2]
        if modes[1] == IntCodeProgram.POSITION_MODE:
            value_b = self.memory[value_b]

        destination = self.memory[self.instruction_pointer + 3]

        if value_a == value_b:
            self.memory[destination] = 1
        else:
            self.memory[destination] = 0
        self.instruction_pointer += 4

    def execute(self):
        """
    Executes the program.

    The 'output' (memory[0]) of the program will be returned.
    """
        if self.instruction_pointer != 0:
            warnings.warn("Program has already executed")
            return self.memory[0]

        while True:
            instruction = self.memory[self.instruction_pointer]
            opcode = instruction % 100
            if opcode == IntCodeProgram.ADD:
                self._add()
            elif opcode == IntCodeProgram.MUL:
                self._mul()
            elif opcode == IntCodeProgram.INPUT:
                self._input()
            elif opcode == IntCodeProgram.OUTPUT:
                self._output()
            elif opcode == IntCodeProgram.JUMP_IF_TRUE:
                self._jump_if_true()
            elif opcode == IntCodeProgram.JUMP_IF_FALSE:
                self._jump_if_false()
            elif opcode == IntCodeProgram.LESS_THAN:
                self._less_than()
            elif opcode == IntCodeProgram.EQUALS:
                self._equals()
            elif opcode == IntCodeProgram.HALT:
                break
            else:
                raise Exception(f'Unrecognized opcode {opcode}')

        return self.memory[0]

    def step(self):
        """
    Executes the program one step at a time.

    Returns True if the program has more steps, and False otherwise.
    """
        instruction = self.memory[self.instruction_pointer]
        opcode = instruction % 100
        if opcode == IntCodeProgram.ADD:
            self._add()
        elif opcode == IntCodeProgram.MUL:
            self._mul()
        elif opcode == IntCodeProgram.INPUT:
            self._input()
        elif opcode == IntCodeProgram.OUTPUT:
            self._output()
        elif opcode == IntCodeProgram.JUMP_IF_TRUE:
            self._jump_if_true()
        elif opcode == IntCodeProgram.JUMP_IF_FALSE:
            self._jump_if_false()
        elif opcode == IntCodeProgram.LESS_THAN:
            self._less_than()
        elif opcode == IntCodeProgram.EQUALS:
            self._equals()
        elif opcode == IntCodeProgram.HALT:
            return False
        else:
            raise Exception(f'Unrecognized opcode {opcode}')

        return True

    def provide_input(self, new_input=[]):
        """Give additional input to the program."""
        self._user_input.extend(new_input)

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "memory") and hasattr(other, "ip")

    def __str__(self):
        return f'Memory: {self.memory}, IP: {self.instruction_pointer}'

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not IntCodeProgram._is_valid_operand(other):
            return NotImplemented

        return self.memory == other.memory and self.instruction_pointer == other.ip

    def __ne__(self, other):
        if not IntCodeProgram._is_valid_operand(other):
            return NotImplemented

        return self.memory != other.memory or self.instruction_pointer != other.ip


########### END py ###########

############## day7.py ###############

import argparse
from itertools import permutations
import os



def part_1(program_text):
    phase_setting_sequences = permutations(range(0, 5))
    outf = open("day07/run2", "w")
    max_thruster_signal = 0
    phase_sequence = None
    for phase_setting_sequence in phase_setting_sequences:
        input_1 = [phase_setting_sequence[0], 0]
        program_1 = IntCodeProgram.from_text(program_text,
                                                     user_input=input_1)
        program_1.execute()

        input_2 = [phase_setting_sequence[1], program_1.output[0]]
        program_2 = IntCodeProgram.from_text(program_text,
                                                     user_input=input_2)
        program_2.execute()

        input_3 = [phase_setting_sequence[2], program_2.output[0]]
        program_3 = IntCodeProgram.from_text(program_text,
                                                     user_input=input_3)
        program_3.execute()

        input_4 = [phase_setting_sequence[3], program_3.output[0]]
        program_4 = IntCodeProgram.from_text(program_text,
                                                     user_input=input_4)
        program_4.execute()

        input_5 = [phase_setting_sequence[4], program_4.output[0]]
        program_5 = IntCodeProgram.from_text(program_text,
                                                     user_input=input_5)
        program_5.execute()
        outf.write(f"{program_5.output[0]} : {str(phase_setting_sequence)}\n")
        if program_5.output[0] > max_thruster_signal:
            max_thruster_signal = program_5.output[0]
            phase_sequence = str(phase_setting_sequence)

    print(
        f'Max Thruster Signal: {max_thruster_signal} with phase sequence {phase_sequence}'
    )


def part_2(program_text):
    phase_setting_sequences = permutations(range(5, 10))
    max_thruster_signal = 0
    phase_sequence = None
    for phase_setting_sequence in phase_setting_sequences:
        programs = list()
        halted = set()
        for index in range(0, 5):
            programs.append(
                IntCodeProgram.from_text(
                    program_text, user_input=[phase_setting_sequence[index]]))
        programs[0].provide_input([0])

        program_5_output = list()
        while len(halted) != len(programs):
            for index in range(0, 5):
                if index in halted:
                    pass
                if not programs[index].step():
                    halted.add(index)

                next_program_index = index + 1
                if next_program_index == 5:
                    next_program_index = 0
                if len(programs[index].output) > 0:
                    programs[next_program_index].provide_input(
                        programs[index].output)
                    if index == 4:
                        program_5_output.extend(programs[index].output)
                    programs[index].output = list()

        if program_5_output[-1] > max_thruster_signal:
            max_thruster_signal = program_5_output[-1]
            phase_sequence = str(phase_setting_sequence)

    print(
        f'Max Thruster Signal: {max_thruster_signal} with phase sequence {phase_sequence}'
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default='inputs/day07.input')
    parser.add_argument('-p', '--part', choices=[1, 2], default=1, type=int)
    args = parser.parse_args()

    program_text = None
    with open(args.filename, 'r') as file:
        program_text = file.read()

    if args.part == 1:
        part_1(program_text)
    else:
        part_2(program_text)


if __name__ == "__main__":
    main()
