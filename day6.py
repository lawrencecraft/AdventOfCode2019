from typing import List
from typing import Tuple

from collections import defaultdict

def loadOrbits() -> List[Tuple[str, str]]:
    with open("input_day6") as f:
        return [tuple(o.strip().split(')')) for o in f.readlines()] 


def solveIt(orbits: List[Tuple[str, str]]):
    childToParent = {}
    for p, c in orbits:
        childToParent[c] = p

    memoized_orbits = {}
    def countOrbits(c):
        if c in memoized_orbits:
            return memoized_orbits[c]
        elif c not in childToParent:
            return 0
        else:
            orbs = 1 + countOrbits(childToParent[c])
            memoized_orbits[c] = orbs
            return orbs
    return sum(countOrbits(c) for c in childToParent)

if __name__ == "__main__":
    orbits = loadOrbits()
    print(solveIt(orbits))
