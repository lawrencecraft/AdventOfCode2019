from typing import List
from typing import Set
from typing import Tuple

from collections import defaultdict

def loadOrbits() -> List[Tuple[str, str]]:
    with open("input_day6") as f:
        return [tuple(o.strip().split(')')) for o in f.readlines()] 


def solveIt(orbits: List[Tuple[str, str]]):
    childToParent = {}
    for p, c in orbits:
        childToParent[c] = p

    current = childToParent['YOU']
    targ = childToParent['SAN']
    def pathToCom(c) -> Set[str]:
        if c not in childToParent:
            return {c}
        else:
            k = pathToCom(childToParent[c])
            k.add(c)
            return k

    return len(pathToCom(current).symmetric_difference(pathToCom(targ)))

if __name__ == "__main__":
    orbits = loadOrbits()
    print(solveIt(orbits))
