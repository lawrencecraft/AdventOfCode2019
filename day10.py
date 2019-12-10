from math import atan2
import itertools


if __name__ == "__main__":
    field = []
    with open("input_day10") as f:
        field = [l.strip() for l in f.readlines()]

    height = len(field)
    width = len(field[0])

    asteroids = {(x, y) for y, row in enumerate(field)
                 for x, square in enumerate(field[y]) if square == '#'}

    def calculateVisible(point):
        return len({atan2(a[1]-point[1], a[0]-point[0]) for a in asteroids if a != point})

    base = max(asteroids, key=calculateVisible)
    print(base)
    print(calculateVisible(base))
