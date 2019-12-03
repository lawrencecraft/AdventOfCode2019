
from typing import NamedTuple

POINT_OPS = {
    "D": lambda p, m: (p[0], p[1] - m),
    "U": lambda p, m: (p[0], p[1] + m),
    "L": lambda p, m: (p[0] - m, p[1]),
    "R": lambda p, m: (p[0] + m, p[1])
}

class Segment(NamedTuple):
    direction: str
    length: int

    @staticmethod
    def parse(line):
        direction = line[0]
        length = int(line[1:])

        return Segment(direction, length)

    def enumeratePoints(self, start):
        movementOp = POINT_OPS[self.direction]
        for m in range(self.length):
            yield movementOp(start, m + 1)

def parseSegments(ln):
    return map(Segment.parse, ln.split(","))

def enumerateAllPoints(segments):
    points = set()
    currentPoint = (0, 0)
    for segment in segments:
        for p in segment.enumeratePoints(currentPoint):
            points.add(p)
            currentPoint = p
    return points

def manhattan(p):
    x, y = p
    return abs(x) + abs(y)

def solveIt():
    firstLine = "a"
    secondLine = "b"
    with open("input_day3") as f:
        firstLine, secondLine = f.readlines()

    firstSegments = parseSegments(firstLine.strip())
    secondSegments = parseSegments(secondLine.strip())

    allFirstSegmentPoints = enumerateAllPoints(firstSegments)
    allSecondSegmentPoints = enumerateAllPoints(secondSegments)

    overlaps = min(manhattan(s) for s in allFirstSegmentPoints.intersection(allSecondSegmentPoints) if s != (0, 0))

    print(overlaps)


if __name__ == "__main__":
    solveIt()