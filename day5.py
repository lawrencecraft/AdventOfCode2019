import sys

from typing import NamedTuple
from typing import List

OPCODE_ADD = 1
OPCODE_MUL = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_HCF = 99

MODE_DIRECT = 1
MODE_POSITION = 0

class Instruction(NamedTuple):
    opcode: int
    arg1_mode: int
    arg2_mode: int
    arg3_mode: int

class ProgramResult(NamedTuple):
    ram: List[int]
    output: List[int]

def resolve(value, mode, programSpace):
    if mode == MODE_DIRECT:
        return value
    elif mode == MODE_POSITION:
        return programSpace[value]
    else:
        raise Exception(f"Unknown mode: {mode}")


def parseInstruction(val) -> Instruction:
    code = val % 100
    modes = val // 100
    mode1 = modes % 10
    mode2 = (modes // 10) % 10
    mode3 = (modes // 100) % 10

    return Instruction(opcode = code, arg1_mode = mode1, arg2_mode = mode2, arg3_mode = mode3)


def executeInstruction(index, instruction, programSpace, transform):
    src1, src2, dst = programSpace[index + 1:index + 4]
    val1 = resolve(src1, instruction.arg1_mode, programSpace)
    val2 = resolve(src2, instruction.arg2_mode, programSpace)
    programSpace[dst] = transform(val1, val2)



def processInstruction(index, programSpace) -> bool:
    rawValue = programSpace[index]
    instruction = parseInstruction(rawValue)
    if instruction.opcode == OPCODE_ADD:
        executeInstruction(index, instruction, programSpace, lambda x, y: x + y)
        return 4
    elif instruction.opcode == OPCODE_MUL:
        executeInstruction(index, instruction, programSpace, lambda x, y: x * y)
        return 4
    elif instruction.opcode == OPCODE_OUTPUT:
        val = programSpace[index + 1]
        print(resolve(val, instruction.arg1_mode, programSpace))

        return 2
        
    elif instruction.opcode == OPCODE_INPUT:
        val = int(sys.stdin.readline().strip())
        dest = programSpace[index + 1]
        programSpace[dest] = val

        return 2
    elif instruction.opcode == OPCODE_HCF:
        return 0
    else:
        raise Exception(f"Unparseable opcode: {rawValue}")


def runProgram(initialRam) -> ProgramResult:
    programSpace = initialRam.copy()
    instructionPointer = 0

    programSize = len(programSpace)

    while instructionPointer < programSize:
        pointerMovement = processInstruction(instructionPointer, programSpace)

        if not pointerMovement:
            break

        instructionPointer += pointerMovement


def doIt():
    ops = []
    with open("input_day5") as f:
        ops = list(map(int, f.read().split(',')))

    runProgram(ops)

if __name__ == "__main__":
    doIt()