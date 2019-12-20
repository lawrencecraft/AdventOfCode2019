from typing import NamedTuple, Tuple

from collections import deque, defaultdict

import heapq

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

def solveMazeFast(maze):
    interestingPlaces = {}
    adjacency = defaultdict(dict)
    allKeys = set()

    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            if c.isalpha() or c == MAZE_ENTRANCE:
                interestingPlaces[c] = (x, y)
                if c.islower():
                    allKeys.add(c)


    height = len(maze)
    width = len(maze[0])
    keyString = ''.join(sorted(allKeys))


    def getNeighboringSquares(pos):
        # value, position where not visited
        for n in NEIGHBORS:
            nx, ny = n[0] + pos[0], n[1] + pos[1]
            if nx >= 0 and nx < width and ny >= 0 and ny < height: 
                v = maze[ny][nx]
                if v != MAZE_WALL:
                    yield v, (nx, ny)

    for c, pos in interestingPlaces.items():
        visited = {pos}
        q = deque([(0, pos)])

        while q:
            steps, current = q.popleft()
            for v, p in getNeighboringSquares(current):
                if v in interestingPlaces and p not in visited:
                    adjacency[c][v] = steps + 1
                elif p not in visited:
                    q.append((steps + 1, p))
                    visited.add(p)

    # Do djikstras on our collapsed graph
    distances = {(MAZE_ENTRANCE, ""): 0}
    
    q = []
    # In the queue: distance, node, keys
    heapq.heappush(q, (0, MAZE_ENTRANCE, ""))

    while q:
        distance, node, keys = heapq.heappop(q)
        if (node, keys) in distances and distances[(node, keys)] < distance:
            continue
        distances[(node, keys)] = distance
        if keys == keyString:
            return distance
        reachableNeighbors = adjacency[node]

        for neighbor, cost in reachableNeighbors.items():
            newKeys = keys
            if neighbor.islower() and neighbor not in keys:
                newKeys = ''.join(sorted(keys + neighbor))
            if neighbor.isupper() and neighbor.lower() not in keys:
                continue
            heapq.heappush(q, (distance + cost, neighbor, newKeys))


    print(adjacency)

    

    


if __name__ == "__main__":
    maze = []
    with open("input_day18") as f:
        maze = list(m.strip() for m in f.readlines())
    print(solveMazeFast(maze))
