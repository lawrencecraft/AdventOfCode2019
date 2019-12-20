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
    adjacency = {'@': {'q': 10, 'Q': 23, 'C': 65, 'z': 68, 'Z': 79, 'm': 104, 'I': 171, 's': 218, 'S': 225}, 'Z': {'M': 40, 'T': 56, '@': 79, 'q': 89, 'Q': 100, 'C': 136, 'z': 145, 'm': 181, 'I': 248, 's': 295, 'S': 302}, 'M': {'T': 18, 'Z': 40}, 'T': {'V': 16, 'M': 18, 'Z': 56}, 'V': {'T': 16, 'b': 47}, 'Q': {'a': 7, '@': 23, 'q': 31, 'C': 86, 'z': 91, 'Z': 100, 'm': 127, 'I': 194, 's': 197, 'S': 248}, 'C': {'x': 23, '@': 65, 'q': 75, 'Q': 86, 'z': 131, 'Z': 136, 'm': 167, 'I': 234, 's': 281, 'S': 288}, 'F': {'k': 7, 'f': 11}, 'J': {'l': 3, 'j': 17}, 'L': {'l': 15, 'f': 21}, 'O': {'h': 3, 'o': 15, 'j': 39}, 'K': {'d': 5, 'k': 11}, 'D': {'d': 11, 'y': 11}, 'X': {'v': 45, 'c': 53, 'q': 91, 'A': 124}, 'P': {'g': 7, 'p': 9}, 'E': {'H': 38, 'W': 38, 'U': 44}, 'H': {'E': 38, 'W': 70, 'U': 76}, 'Y': {'p': 9, 'y': 11}, 'W': {'o': 23, 'U': 24, 'E': 38, 'H': 70}, 'B': {'u': 43, 't': 91}, 'G': {'n': 7, 'g': 13}, 'N': {'n': 7}, 'A': {'q': 37, 't': 75, 'c': 79, 'X': 124}, 'R': {'I': 18}, 'U': {'S': 18, 'W': 24, 'E': 44, 'H': 76}, 'S': {'U': 18, 'I': 80, 'z': 165, 'm': 181, '@': 225, 'q': 233, 'Q': 248, 'C': 288, 'Z': 302, 's': 443}, 'I': {'R': 18, 'S': 80, 'z': 111, 'm': 127, '@': 171, 'q': 179, 'Q': 194, 'C': 234, 'Z': 248, 's': 389}, 'b': {'V': 47}, 'i': {'w': 94, 'a': 134}, 'a': {'Q': 7, 'i': 134}, 'e': {'w': 20}, 'w': {'e': 20, 'i': 94}, 'x': {'C': 23}, 's': {'Q': 197, '@': 218, 'q': 226, 'C': 281, 'z': 286, 'Z': 295, 'm': 322, 'I': 389, 'S': 443}, 'h': {'O': 3}, 'c': {'q': 46, 'X': 53, 'A': 79}, 'l': {'J': 3, 'L': 15, 'f': 22}, 'j': {'J': 17, 'o': 36, 'O': 39}, 'f': {'F': 11, 'L': 21, 'l': 22}, 'q': {'@': 10, 'Q': 31, 'A': 37, 'c': 46, 'C': 75, 'z': 76, 'Z': 89, 'X': 91, 'm': 112, 'I': 179, 's': 226, 'S': 233}, 'k': {'F': 7, 'K': 11}, 'd': {'K': 5, 'D': 11}, 'u': {'B': 43, 't': 116}, 'g': {'P': 7, 'G': 13}, 'v': {'r': 40, 'X': 45}, 'o': {'O': 15, 'W': 23, 'j': 36}, 'p': {'P': 9, 'Y': 9}, 'y': {'D': 11, 'Y': 11}, 'm': {'z': 44, '@': 104, 'q': 112, 'Q': 127, 'I': 127, 'C': 167, 'Z': 181, 'S': 181, 's': 322}, 'r': {'v': 40}, 'n': {'N': 7, 'G': 7}, 'z': {'m': 44, '@': 68, 'q': 76, 'Q': 91, 'I': 111, 'C': 131, 'Z': 145, 'S': 165, 's': 286}, 't': {'A': 75, 'B': 91, 'u': 116}}
    # return
    q = []
    # In the queue: distance, node, keys
    heapq.heappush(q, (0, MAZE_ENTRANCE, ""))

    while q:
        distance, node, keys = heapq.heappop(q)
        if keys == keyString:
            return distance
        reachableNeighbors = adjacency[node]

        for neighbor, cost in reachableNeighbors.items():
            newKeys = keys
            if neighbor.islower() and neighbor not in keys:
                newKeys = ''.join(sorted(keys + neighbor))
            if neighbor.isupper() and neighbor.lower() not in keys:
                continue
            if (neighbor, newKeys) not in distances or distances[(neighbor, newKeys)] > distance + cost:
                distances[(neighbor, newKeys)] = distance + cost
                heapq.heappush(q, (distance + cost, neighbor, newKeys))


    print(adjacency)

    

    


if __name__ == "__main__":
    maze = []
    with open("input_day18") as f:
        maze = list(m.strip() for m in f.readlines())
    print(solveMazeFast(maze))
