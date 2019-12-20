from typing import NamedTuple, Tuple

from collections import deque

class MazeGraphNode(NamedTuple):
    pos: Tuple[int, int]
    keys: str

MAZE_WALL = '#'
MAZE_NORMAL = '.'
MAZE_ENTRANCE = '@'

NEIGHBORS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]

def solveMaze(maze):
    entrance = None
    keys = set()
    
    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            if c.islower():
                keys.add(c)
            elif c == MAZE_ENTRANCE:
                entrance = (x, y)

    initialState = MazeGraphNode(pos=entrance, keys='')
    states = deque([(0, initialState)])
    visited = {initialState}
    keyString = ''.join(sorted(keys)).upper()

    height = len(maze)
    width = len(maze[0])


    def getNeighboringSquares(node: MazeGraphNode):
        # value, position where not visited
        for n in NEIGHBORS:
            nx, ny = n[0] + node.pos[0], n[1] + node.pos[1]
            if nx >= 0 and nx < width and ny >= 0 and ny < height: 
                v = maze[ny][nx]
                if (v.isupper() and v in node.keys) or v.islower() or v == MAZE_NORMAL or v == MAZE_ENTRANCE:
                    yield v, (nx, ny)

    while states:
        steps, currentState = states.popleft()

        for value, position in getNeighboringSquares(currentState):
            newStatePosition = position
            newStateKeys = currentState.keys

            if value.islower() and value.upper() not in currentState.keys:
                newStateKeys = ''.join(sorted(newStateKeys + value.upper()))
                if newStateKeys == keyString:
                    # We have found them all
                    return steps + 1

            newState = MazeGraphNode(pos = position, keys = newStateKeys)
            
            if newState not in visited:
                visited.add(newState)
                states.append((steps + 1, newState))


if __name__ == "__main__":
    maze = []
    with open("input_day18") as f:
        maze = list(m.strip() for m in f.readlines())
    print(solveMaze(maze))
