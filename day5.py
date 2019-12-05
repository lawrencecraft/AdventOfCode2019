import sys

from typing import NamedTuple
from typing import List

OPCODE_ADD = 1
OPCODE_MUL = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4

OPCODE_JMPTRUE = 5
OPCODE_JMPFALSE = 6
OPCODE_LESSTHAN = 7
OPCODE_EQUALS = 8

OPCODE_HCF = 99

MODE_DIRECT = 1
MODE_POSITION = 0

MOVEMENT_RELATIVE=1
MOVEMENT_ABSOLUTE=2
MOVEMENT_HALT=3

class Instruction(NamedTuple):
    opcode: int
    arg1_mode: int
    arg2_mode: int
    arg3_mode: int

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

def extractParameters(index, instruction, programSpace):
    src1, src2 = programSpace[index + 1:index + 3]
    val1 = resolve(src1, instruction.arg1_mode, programSpace)
    val2 = resolve(src2, instruction.arg2_mode, programSpace)

    return val1, val2

def extractParametersAndDestination(index, instruction, programSpace):
    val1, val2 = extractParameters(index, instruction, programSpace)
    dst = programSpace[index + 3]
    return val1, val2, dst

def executeInstruction(index, instruction, programSpace, transform):
    val1, val2, dst = extractParametersAndDestination(index, instruction, programSpace)
    programSpace[dst] = transform(val1, val2)

def executeConditionalJump(index, instruction, programSpace, test) -> bool:
    val1, val2 = extractParameters(index, instruction, programSpace)
    if test(val1):
        return val2, MOVEMENT_ABSOLUTE
    else:
        return 3, MOVEMENT_RELATIVE

def executeComparison(index, instruction, programSpace, test):
    val1, val2, dst = extractParametersAndDestination(index, instruction, programSpace)
    if test(val1, val2):
        programSpace[dst] = 1
    else:
        programSpace[dst] = 0
    
    return 4, MOVEMENT_RELATIVE

def processInstruction(index, programSpace) -> bool:
    rawValue = programSpace[index]
    instruction = parseInstruction(rawValue)

    if instruction.opcode == OPCODE_ADD:
        executeInstruction(index, instruction, programSpace, lambda x, y: x + y)
        return 4, MOVEMENT_RELATIVE

    elif instruction.opcode == OPCODE_MUL:
        executeInstruction(index, instruction, programSpace, lambda x, y: x * y)
        return 4, MOVEMENT_RELATIVE

    elif instruction.opcode == OPCODE_OUTPUT:
        val = programSpace[index + 1]
        print(resolve(val, instruction.arg1_mode, programSpace))
        return 2, MOVEMENT_RELATIVE

    elif instruction.opcode == OPCODE_INPUT:
        val = int(sys.stdin.readline().strip())
        dest = programSpace[index + 1]
        programSpace[dest] = val
        return 2, MOVEMENT_RELATIVE

    elif instruction.opcode == OPCODE_JMPTRUE:
        return executeConditionalJump(index, instruction, programSpace, lambda x: x)

    elif instruction.opcode == OPCODE_JMPFALSE:
        return executeConditionalJump(index, instruction, programSpace, lambda x: not x)

    elif instruction.opcode == OPCODE_LESSTHAN:
        return executeComparison(index, instruction, programSpace, lambda x, y: x < y)

    elif instruction.opcode == OPCODE_EQUALS:
        return executeComparison(index, instruction, programSpace, lambda x, y: x == y)

    elif instruction.opcode == OPCODE_HCF:
        return 0, MOVEMENT_HALT

    else:
        raise Exception(f"Unparseable opcode: {rawValue}")


def runProgram(initialRam):
    programSpace = initialRam.copy()
    instructionPointer = 0

    programSize = len(programSpace)

    while instructionPointer < programSize:
        pointerMovement, movementType = processInstruction(instructionPointer, programSpace)

        if movementType == MOVEMENT_HALT:
            break
        elif movementType == MOVEMENT_RELATIVE:
            instructionPointer += pointerMovement
        elif movementType == MOVEMENT_ABSOLUTE:
            instructionPointer = pointerMovement
        else:
            raise Exception(f"Unknown movement type: {movementType}")

def doIt():
    ops = []
    with open("input_day5") as f:
        ops = list(map(int, f.read().split(',')))

    runProgram(ops)

if __name__ == "__main__":
    doIt()