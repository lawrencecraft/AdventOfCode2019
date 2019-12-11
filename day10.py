from math import atan2, pi

import itertools


if __name__ == "__main__":
    field = []
    with open("input_day10") as f:
        field = [l.strip() for l in f.readlines()]

    height = len(field)
    width = len(field[0])

   # We're going clockwise from the top - angle must be translated
    def getAngle(p1, p2):
        def norm(a): return (2*pi + a) % (2*pi)
        normalizedAngle = norm(atan2(p2[1]-p1[1], p2[0]-p1[0])) # normalize the angle to get rid of any negatives - just rads from horizontal
        return norm(normalizedAngle+pi/2) # we are offset from vertical

    asteroids = {(x, y) for y, row in enumerate(field)
                 for x, square in enumerate(field[y]) if square == '#'}

    def calculateVisible(point):
        return len({getAngle(point, a) for a in asteroids if a != point})

    base = max(asteroids, key=calculateVisible)
    print(base)
    print(calculateVisible(base))

    from collections import defaultdict
    byAngle = defaultdict(list)
    for a in asteroids:
        byAngle[getAngle(base, a)].append(a)

    def manhattan(p1, p2):
        return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

    targetList = [sorted(x[1], key=lambda x: manhattan(base, x))
                  for x in sorted(byAngle.items(), key=lambda x: x[0])]

    targetsKilled = 0
    while targetList:
        for target in targetList:
            targetsKilled += 1
            blasted = target.pop(0)
            if targetsKilled == 200:
                print(f"200th is {blasted}")
        targetList = [t for t in targetList if t]
