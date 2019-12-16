import sys

from typing import NamedTuple
from typing import List
from typing import Tuple
from typing import Callable

from itertools import permutations

import time

OPCODE_ADD = 1
OPCODE_MUL = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4

OPCODE_JMPTRUE = 5
OPCODE_JMPFALSE = 6
OPCODE_LESSTHAN = 7
OPCODE_EQUALS = 8

OPCODE_SETREL = 9

OPCODE_HCF = 99

MODE_RELATIVE = 2
MODE_DIRECT = 1
MODE_POSITION = 0

MOVEMENT_RELATIVE = 1
MOVEMENT_ABSOLUTE = 2
MOVEMENT_HALT = 3


class Instruction(NamedTuple):
    opcode: int
    arg1_mode: int
    arg2_mode: int
    arg3_mode: int


class Memory(object):
    def __init__(self, initialProgramRam=[], pageSize=1024):
        self.__pageMap__ = {}
        self.__pageSize__ = pageSize
        for address, v in enumerate(initialProgramRam):
            self.setValue(address, v)

    def access(self, address: int) -> int:
        if address < 0:
            raise Exception(
                "Attempted to access a negative address. This isn't good.")
        page, offset = self.__mapToPage__(address)
        if page in self.__pageMap__:
            return self.__pageMap__[page][offset]
        else:
            return 0

    def setValue(self, address, value):
        page, offset = self.__mapToPage__(address)
        if page in self.__pageMap__:
            self.__pageMap__[page][offset] = value
        else:
            newPage = [0] * self.__pageSize__
            newPage[offset] = value
            self.__pageMap__[page] = newPage

    def __getitem__(self, address):
        return self.access(address)

    def __setitem__(self, address, value):
        self.setValue(address, value)

    def __mapToPage__(self, address: int) -> Tuple[int, int]:
        return (address // self.__pageSize__, address % self.__pageSize__)

    def __repr__(self):
        return f"Memory(pageSize={self.__pageSize__}, realPages={len(self.__pageMap__)}, pages={self.__pageMap__})"


class Offsets(object):
    def __init__(self):
        self.offset = 0

    def moveOffset(self, value):
        self.offset += value


class ProgramState(NamedTuple):
    memory: Memory
    instructionPointer: int
    inputDestination: int
    outputHandler: Callable[[int], None]
    relativeOffset: Offsets


def resolve(value, mode, programState: ProgramState):
    if mode == MODE_DIRECT:
        return value
    elif mode == MODE_POSITION:
        return programState.memory[value]
    elif mode == MODE_RELATIVE:
        return programState.memory[programState.relativeOffset.offset + value]
    else:
        raise Exception(f"Unknown mode: {mode}")


def parseInstruction(val) -> Instruction:
    code = val % 100
    modes = val // 100
    mode1 = modes % 10
    mode2 = (modes // 10) % 10
    mode3 = (modes // 100) % 10

    return Instruction(opcode=code, arg1_mode=mode1, arg2_mode=mode2, arg3_mode=mode3)


def extractParameters(index, instruction, programState: ProgramState):
    src1 = programState.memory[index + 1]
    src2 = programState.memory[index + 2]
    val1 = resolve(src1, instruction.arg1_mode, programState)
    val2 = resolve(src2, instruction.arg2_mode, programState)

    return val1, val2


def resolveDestination(index, mode, programState: ProgramState):
    dst = programState.memory[index]
    if mode == MODE_RELATIVE:
        dst += programState.relativeOffset.offset

    return dst


def extractParametersAndDestination(index, instruction, programState: ProgramState):
    val1, val2 = extractParameters(index, instruction, programState)
    dst = resolveDestination(index + 3, instruction.arg3_mode, programState)
    return val1, val2, dst


def executeInstruction(index, instruction, programState: ProgramState, transform):
    val1, val2, dst = extractParametersAndDestination(
        index, instruction, programState)
    programState.memory[dst] = transform(val1, val2)


def executeConditionalJump(index, instruction, programState: ProgramState, test) -> bool:
    val1, val2 = extractParameters(index, instruction, programState)

    if test(val1):
        return val2, MOVEMENT_ABSOLUTE
    else:
        return 3, MOVEMENT_RELATIVE


def executeComparison(index, instruction, programState: ProgramState, test):
    val1, val2, dst = extractParametersAndDestination(
        index, instruction, programState)
    if test(val1, val2):
        programState.memory[dst] = 1
    else:
        programState.memory[dst] = 0

    return 4, MOVEMENT_RELATIVE


def processInstruction(index, programState: ProgramState) -> bool:
    rawValue = programState.memory[index]
    instruction = parseInstruction(rawValue)

    if instruction.opcode == OPCODE_ADD:
        executeInstruction(index, instruction,
                           programState, lambda x, y: x + y)
        return 4, MOVEMENT_RELATIVE

    elif instruction.opcode == OPCODE_MUL:
        executeInstruction(index, instruction,
                           programState, lambda x, y: x * y)
        return 4, MOVEMENT_RELATIVE

    elif instruction.opcode == OPCODE_OUTPUT:
        val = programState.memory[index + 1]
        programState.outputHandler(
            resolve(val, instruction.arg1_mode, programState))
        return 2, MOVEMENT_RELATIVE

    elif instruction.opcode == OPCODE_INPUT:
        dest = resolveDestination(index + 1, instruction.arg1_mode, programState)
        state = ProgramState(memory=programState.memory, instructionPointer=index + 2,
                             inputDestination=dest, outputHandler=programState.outputHandler,
                             relativeOffset=programState.relativeOffset)
        return state, MOVEMENT_HALT

    elif instruction.opcode == OPCODE_JMPTRUE:
        return executeConditionalJump(index, instruction, programState, lambda x: x)

    elif instruction.opcode == OPCODE_JMPFALSE:
        return executeConditionalJump(index, instruction, programState, lambda x: not x)

    elif instruction.opcode == OPCODE_LESSTHAN:
        return executeComparison(index, instruction, programState, lambda x, y: x < y)

    elif instruction.opcode == OPCODE_EQUALS:
        return executeComparison(index, instruction, programState, lambda x, y: x == y)

    elif instruction.opcode == OPCODE_HCF:
        return None, MOVEMENT_HALT

    elif instruction.opcode == OPCODE_SETREL:
        relativeDelta = resolve(
            programState.memory[index + 1], instruction.arg1_mode, programState)
        programState.relativeOffset.moveOffset(relativeDelta)
        return 2, MOVEMENT_RELATIVE

    else:
        raise Exception(f"Unparseable opcode: {rawValue}")


def execute(p: ProgramState) -> ProgramState:
    instructionPointer = p.instructionPointer

    while True:  # Execute until we halt, yield for input, or hit an error
        pointerMovement, movementType = processInstruction(
            instructionPointer, p)

        if movementType == MOVEMENT_HALT:
            return pointerMovement  # Could be none -> indicates termination
        elif movementType == MOVEMENT_RELATIVE:
            instructionPointer += pointerMovement
        elif movementType == MOVEMENT_ABSOLUTE:
            instructionPointer = pointerMovement
        else:
            raise Exception(f"Unknown movement type: {movementType}")


def startNew(initialRam, handleOutput) -> ProgramState:
    initialState = ProgramState(
        memory=Memory(initialRam.copy()),
        instructionPointer=0,
        outputHandler=handleOutput,
        inputDestination=None,
        relativeOffset=Offsets())
    return execute(initialState)


def resumeWithInput(programState: ProgramState, value: int):
    if not programState:
        raise Exception("Cannot resume explicitly halted program")
    programState.memory[programState.inputDestination] = value
    return execute(programState)


def startWithStaticInput(initialRam, inputQueue, handleOutput):
    state = startNew(initialRam, handleOutput)
    while state and inputQueue:
        state = resumeWithInput(state, inputQueue.pop(0))

    return state


def runInteractive(initialRam):
    state = startNew(initialRam, lambda x: print(x))
    while state:
        ip = int(sys.stdin.readline().strip())
        state = resumeWithInput(state, ip)

def parseOutput(op):
    for x in range(0, len(op), 3):
        yield tuple(op[x:x+3])



def getTheThings(program):
    op = []
    startNew(program, lambda x: op.append(x))

    print(sum(1 for _,_,b in parseOutput(op) if b == 2))
    print(max(x for x,y,_ in parseOutput(op)))
    print(max(y for x,y,_ in parseOutput(op)))
    print(min(x for x,y,_ in parseOutput(op)))
    print(min(y for x,y,_ in parseOutput(op)))

CHAR_DISPLAY = [' ', '@', '#', '-', 'o']

def render(grid, score):
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')
    for row in grid:
        print(''.join(CHAR_DISPLAY[c] for c in row))
    print(f"Score: {score}")
    time.sleep(.1)

def applyOutput(outputs, grid):
    score = None
    ballX = None
    paddleX = None
    for x,y,t in parseOutput(outputs):
        if x == -1:
            score = t
        else:
            if t == 4:
                ballX = x
            elif t == 3:
                paddleX = x

            grid[y][x] = t
    return score, ballX, paddleX

def direction(paddleX, ballX):
    if paddleX == ballX:
        return 0
    elif paddleX > ballX:
        return 1
    else:
        return -1

def playGame(program):
    program[0] = 2
    op = []
    state = startNew(program, lambda x: op.append(x))
    initialThings = parseOutput(state)

    maxx = max(x for x,y,_ in parseOutput(op)) + 1
    maxy = max(y for x,y,_ in parseOutput(op)) + 1

    grid = [[0] * maxx for _ in range(maxy)]
    score, paddleX, ballX = applyOutput(op, grid)

    # render(grid, score)
    import time

    while state:

        i = direction(paddleX, ballX)
        

        op = []
        state = resumeWithInput(state, i)
        newScore, newPaddleX, newBallX = applyOutput(op, grid)
        score = newScore or score
        paddleX = newPaddleX or paddleX
        ballX = newBallX or ballX
        render(grid, score)

    print(score)




def doIt():
    ops = []
    with open("input_day13") as f:
        ops = list(map(int, f.read().split(',')))

    playGame(ops)


if __name__ == "__main__":
    doIt()
