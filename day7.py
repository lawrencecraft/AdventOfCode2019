import sys

from typing import NamedTuple
from typing import List
from typing import Tuple
from typing import Callable

from itertools import permutations

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

class ProgramState(NamedTuple):
    memory: List[int]
    instructionPointer: int
    inputDestination: int
    outputHandler: Callable[[int], None]

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

def processInstruction(index, programSpace, handleOutput) -> bool:
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
        handleOutput(resolve(val, instruction.arg1_mode, programSpace))
        return 2, MOVEMENT_RELATIVE

    elif instruction.opcode == OPCODE_INPUT:
        dest = programSpace[index + 1]
        state = ProgramState(memory = programSpace, instructionPointer = index + 2, inputDestination = dest, outputHandler = handleOutput)
        return state, MOVEMENT_HALT

    elif instruction.opcode == OPCODE_JMPTRUE:
        return executeConditionalJump(index, instruction, programSpace, lambda x: x)

    elif instruction.opcode == OPCODE_JMPFALSE:
        return executeConditionalJump(index, instruction, programSpace, lambda x: not x)

    elif instruction.opcode == OPCODE_LESSTHAN:
        return executeComparison(index, instruction, programSpace, lambda x, y: x < y)

    elif instruction.opcode == OPCODE_EQUALS:
        return executeComparison(index, instruction, programSpace, lambda x, y: x == y)

    elif instruction.opcode == OPCODE_HCF:
        return None, MOVEMENT_HALT

    else:
        raise Exception(f"Unparseable opcode: {rawValue}")

def execute(p: ProgramState) -> ProgramState:
    programSize = len(p.memory)
    instructionPointer = p.instructionPointer

    while instructionPointer < programSize:
        pointerMovement, movementType = processInstruction(instructionPointer, p.memory, p.outputHandler)

        if movementType == MOVEMENT_HALT:
            return pointerMovement # Could be none -> indicates termination
        elif movementType == MOVEMENT_RELATIVE:
            instructionPointer += pointerMovement
        elif movementType == MOVEMENT_ABSOLUTE:
            instructionPointer = pointerMovement
        else:
            raise Exception(f"Unknown movement type: {movementType}")



def startNew(initialRam, handleOutput) -> ProgramState:
    initialState = ProgramState(memory = initialRam.copy(), instructionPointer = 0, outputHandler = handleOutput, inputDestination = None)
    return execute(initialState)

def resumeWithInput(programState: ProgramState, value: int):
    if not programState:
        raise Exception("Cannot resume explicitly halted program")
    programState.memory[programState.inputDestination] = value
    return execute(programState)

# def staticInput(programState, )

def startWithStaticInput(initialRam, inputQueue, handleOutput):
    state = startNew(initialRam, handleOutput)
    while state and inputQueue:
        state = resumeWithInput(state, inputQueue.pop(0))

    return state



def runMultipleAmplifiers(program: List[int], amplifierPermutation: Tuple[int]):
    numAmplifiers = len(amplifierPermutation)
    outputs = [[] for _ in range(numAmplifiers)]

    def generateOutputHandler(index):
        return lambda x: outputs[index].append(x)

    amplifiers = [startWithStaticInput(program, [amplifierPermutation[i]], generateOutputHandler(i)) for i in range(numAmplifiers)]
    currentInput = 0

    # Run through each program in turn
    while True:
        for i, s in enumerate(amplifiers):
            amplifiers[i] = resumeWithInput(s, currentInput)
            currentInput = outputs[i][-1]
        if not amplifiers[-1]:
            return currentInput




def doIt():
    ops = []
    with open("input_day7") as f:
        ops = list(map(int, f.read().split(',')))

    print(max(runMultipleAmplifiers(ops, p) for p in permutations([9,8,7,6,5])))


if __name__ == "__main__":
    doIt()