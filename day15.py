import sys

from typing import NamedTuple
from typing import List
from typing import Tuple
from typing import Callable

from itertools import permutations

from intcode import startNew, resumeWithInput, ProgramState

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

def getMaze(maze, p):
    x, y = p
    if x < 0 or y < 0:
        raise Exception("Index out of range")
    return maze[y][x]

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
            points = [Runner(state.fork(state.outputHandler), currentPosition, d) for d in DIRS if d != direction and getMaze(maze, applyDirection(currentPosition, d)) == MAZE_UNKNOWN]

            pendingJunctions.extend(points)

            nextPoint = applyDirection(currentPosition, direction)
            # Have we already been where we're about to go? No need to revisit.
            if getMaze(maze, nextPoint) != MAZE_UNKNOWN:
                break

            # Run as far as we can in a straight line
            state = resumeWithInput(state, direction)
            result = output.pop(0)

            if result == 0:
                # It is a wall. We can go no further
                setMaze(maze, nextPoint, MAZE_WALL)
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
