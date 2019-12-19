import sys

from typing import NamedTuple
from typing import List
from typing import Set
from typing import Tuple
from typing import Callable

from intcode import startNew, startWithStaticInput


def captureImage(program):
    output = [[]]

    def handleOutput(x):
        if x == 10:
            output.append([])
        else:
            output[-1].append(chr(x))
    startNew(program, handleOutput)

    return [o for o in output if o]


def render(image, points):
    import sys
    points = set(points)
    for y, row in enumerate(image):
        for x, c in enumerate(row):
            if (x, y) in points:
                c = 'O'
            sys.stdout.write(c)
        sys.stdout.write('\n')


NEIGHBORS = [
    (0, 1),
    (0, -1),
    (-1, 0),
    (1, 0)
]


def findIntersections(image):
    def isIntersection(x, y):
        for dx, dy in NEIGHBORS:
            if image[y + dy][x + dx] != '#':
                return False
        return True

    for y, row in enumerate(image[1:-1]):
        for x, c in enumerate(row[1:-1]):
            if c == '#':
                realX, realY = x+1, y+1  # Reapply our offsets
                if isIntersection(realX, realY):
                    yield (realX, realY)


class Decision(NamedTuple):
    currentDirection: Tuple[int, int]
    visited: Set[int]
    location: Tuple[int, int]
    pathSoFar: str


def generateNaivePath(image):
    # North, East, South, West
    # Right -> +1
    # Left -> -1
    movement = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    movementTypes = {
        '^': 0,
        '>': 1,
        'v': 2,
        '<': 3
    }
    currentLocation = None
    currentDirection = None

    height = len(image)
    width = len(image[0])

    for y, row in enumerate(image):
        for x, c in enumerate(row):
            if c in movementTypes:
                currentLocation = (x, y)
                currentDirection = movement[movementTypes[c]]

    def applyDirection(p, d):
        return (p[0] + d[0], p[1] + d[1])

    def getImage(p):
        x, y = p
        if x < width and y < height:
            return image[y][x]
        else:
            return None

    def canMove(p, d):
        return getImage(applyDirection(p, d)) == '#'

    def getPossibleDirections(p, d):
        i = movement.index(d)
        left = movement[(i - 1) % len(movement)]
        right = movement[(i + 1) % len(movement)]

        if getImage(applyDirection(p, left)) == '#':
            return "L", left

        if getImage(applyDirection(p, right)) == '#':
            return "R", right

        return None, None

    currentStreak = 0
    streaks = []
    while True:
        if canMove(currentLocation, currentDirection):
            currentLocation = applyDirection(currentLocation, currentDirection)
            currentStreak += 1
        else:
            # We cannot move. Dis bad.
            turnType, currentDirection = getPossibleDirections(
                currentLocation, currentDirection)
            if currentStreak:
                lastTurn = streaks.pop()
                streaks.append(lastTurn + str(currentStreak))

            currentStreak = 0
            if turnType is None:
                # We done
                return streaks
            streaks.append(turnType)


def compressPath(stringPath):
    # Brute force this fool. Nothing can be more than 20 chrs long.
    for aLength in range(19):
        for bLength in range(19):
            for cLength in range(19):
                a = stringPath[:aLength+1]
                noAs = stringPath.replace(a, "")
                b = noAs[:bLength + 1]
                noBs = noAs.replace(b, "")
                c = noBs[:cLength + 1]
                noCs = noBs.replace(c, "")
                if not noCs:
                    return a, b, c


def splitUpSentence(s):
    buf = ""
    for c in s:
        if c == 'L' or c == 'R':
            if buf:
                yield buf
                buf = ""
            yield c
        else:
            buf += c

    yield buf


def executeHoover(program, mainMovementString, movementProgram):
    program[0] = 2
    mainProgram = ','.join(mainMovementString)
    programDefinitions = list(map(','.join, map(splitUpSentence, movementProgram)))
    showFeed = 'n'

    inputString = '\n'.join([mainProgram] + programDefinitions + [showFeed]) + '\n'
    fullInput = list(map(ord, inputString))

    op = []
    startWithStaticInput(program, fullInput, lambda x: op.append(x))
    print(op[-1])


def doIt():
    ops = []
    with open("input_day17") as f:
        ops = list(map(int, f.read().split(',')))

    image = captureImage(ops)
    points = set(findIntersections(image))
    render(image, points)
    print(sum(map(lambda x: x[0]*x[1], points)))
    initialPath = generateNaivePath(image)
    stringPath = ''.join(initialPath)
    print(stringPath)

    a, b, c = compressPath(stringPath)
    overallMovement = stringPath.replace(
        a, "A").replace(b, "B").replace(c, "C")
    print(overallMovement)

    executeHoover(ops, overallMovement, [a, b, c])


if __name__ == "__main__":
    doIt()
