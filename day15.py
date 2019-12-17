import sys

from typing import NamedTuple
from typing import List
from typing import Tuple
from typing import Callable

from itertools import permutations

import copy

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

    def fork(self):
        newMemory = Memory()
        newMemory.__pageSize__ = self.__pageSize__
        newMemory.__pageMap__ = copy.deepcopy(self.__pageMap__)
        return newMemory

    def __getitem__(self, address):
        return self.access(address)

    def __setitem__(self, address, value):
        self.setValue(address, value)

    def __mapToPage__(self, address: int) -> Tuple[int, int]:
        return (address // self.__pageSize__, address % self.__pageSize__)

    def __repr__(self):
        return f"Memory(pageSize={self.__pageSize__}, realPages={len(self.__pageMap__)}, pages={self.__pageMap__})"


class Offsets(object):
    def __init__(self, initialOffset=0):
        self.offset = initialOffset

    def moveOffset(self, value):
        self.offset += value


class ProgramState(NamedTuple):
    memory: Memory
    instructionPointer: int
    inputDestination: int
    outputHandler: Callable[[int], None]
    relativeOffset: Offsets

    def fork(self, outputHandler) -> NamedTuple:
        ram = self.memory.fork()
        offset = Offsets(self.relativeOffset.offset)

        return ProgramState(memory=ram,
                            relativeOffset=offset, 
                            instructionPointer=self.instructionPointer, 
                            outputHandler=outputHandler, 
                            inputDestination=self.inputDestination)


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
        dest = resolveDestination(
            index + 1, instruction.arg1_mode, programState)
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


class Runner(object):
    def __init__(self, state: ProgramState, initialLocation: Tuple[int, int], direction: int):
        self.state = state
        self.location = initialLocation
        self.direction = direction

    def translate(self, x, y):
        self.location = tuple(map(sum, zip(self.location, (x, y))))

DIRS = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}

MAZE_UNKNOWN = -1
MAZE_ORIGIN = 0
MAZE_VISITED = 1
MAZE_TARGET = 2
MAZE_WALL = 3

MAZE_FEATURES = {
    MAZE_UNKNOWN: ' ',
    MAZE_ORIGIN: 'o', # Origin
    MAZE_VISITED: '.',
    MAZE_TARGET: 'X', # Oxygen
    MAZE_WALL: '#' # wall
}

def applyDirection(p, d):
    dx, dy = DIRS[d]
    x, y = p
    if x < 0 or y < 0:
        raise Exception("Index out of range")
    return (x + dx, y + dy)

def setMaze(maze, p, v):
    x, y = p
    if x < 0 or y < 0:
        raise Exception("Index out of range")
    maze[y][x] = v

def renderMaze(maze):
    for row in reversed(maze):
        print(''.join(MAZE_FEATURES[x] for x in row))

def runMaze(program):
    # Just set it big enough so we don't have to worry about expansion
    maze = [[MAZE_UNKNOWN] * 60 for _ in range(60)]
    start = (30, 30)
    setMaze(maze, start, MAZE_ORIGIN)
    output = []
    initialState = startNew(program, lambda x: output.append(x))
    pendingJunctions: List[Runner] = [Runner(initialState, start, 1)]
    visited = set(start)
    oxygen = None

    while pendingJunctions:
        currentRunner = pendingJunctions.pop()
        currentPosition = currentRunner.location
        state = currentRunner.state
        direction = currentRunner.direction
        while True:
            # If we've already visited this node, we don't need to re-queue up runners
            mustCheck = currentPosition not in visited
            visited.add(currentPosition)

            #TODO: Examine states
            if mustCheck:
                points = [Runner(state.fork(state.outputHandler), currentPosition, d) for d in DIRS if d != direction and applyDirection(currentPosition, d) not in visited]

                pendingJunctions.extend(points)

            nextPoint = applyDirection(currentPosition, direction)
            # Have we already been where we're about to go? No need to revisit.
            if nextPoint in visited:
                break

            # Run as far as we can in a straight line
            state = resumeWithInput(state, direction)
            result = output.pop(0)

            if result == 0:
                # It is a wall. We can go no further
                setMaze(maze, nextPoint, MAZE_WALL)
                visited.add(nextPoint)
                break
            elif result == 1:
                setMaze(maze, nextPoint, MAZE_VISITED) 
            elif result == 2:
                setMaze(maze, nextPoint, MAZE_TARGET)
                oxygen = nextPoint
            currentPosition = nextPoint

    return maze, start, oxygen


def findPath(maze, start, target):
    queue = [(0, start)]
    visited = set()

    def getNeighbors(p):
        x, y = p
        points = [tuple(map(sum, zip(d, p))) for d in DIRS.values()]
        return [n for n in points if maze[n[1]][n[0]] != MAZE_WALL and n not in visited]


    while queue:
        cost, position = queue.pop(0)
        visited.add(position)
        
        if position == target:
            return cost
        
        neighbors = getNeighbors(position)
        queue.extend(map(lambda x: (cost + 1, x), neighbors))

def fill(maze, start):
    # Literally the same thing as above, except without an end
    queue = [(0, start)]
    visited = set()

    def getNeighbors(p):
        x, y = p
        points = [tuple(map(sum, zip(d, p))) for d in DIRS.values()]
        return [n for n in points if maze[n[1]][n[0]] != MAZE_WALL and n not in visited]


    while True:
        cost, position = queue.pop(0)
        visited.add(position)
        neighbors = getNeighbors(position)
        queue.extend(map(lambda x: (cost + 1, x), neighbors))
        if not queue:
            return cost

def doIt():
    ops = []
    with open("input_day15") as f:
        ops = list(map(int, f.read().split(',')))

    m, s, t = runMaze(ops)
    renderMaze(m)
    print(findPath(m, s, t))
    print(fill(m, t))


if __name__ == "__main__":
    doIt()
