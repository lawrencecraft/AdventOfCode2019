
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
    points = {}
    currentPoint = (0, 0)
    walked = 0
    for segment in segments:
        for p in segment.enumeratePoints(currentPoint):
            walked += 1
            if p not in points:
                points[p] = walked
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

    allFirstSegmentPointsWithCost = enumerateAllPoints(firstSegments)
    allSecondSegmentPointsWithCost = enumerateAllPoints(secondSegments)
    
    overlaps = allFirstSegmentPointsWithCost.keys() & allSecondSegmentPointsWithCost.keys()
    minCost = min(allFirstSegmentPointsWithCost[p] + allSecondSegmentPointsWithCost[p] for p in overlaps)
    print(minCost)


if __name__ == "__main__":
    solveIt()