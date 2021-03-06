from collections import defaultdict

DIRS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

def solveMaze(maze):
    portalToPoints = defaultdict(list)
    pointToPortals = {}

    def hasPortal(x, y):
        for dy,dx in DIRS:
            mv1 = maze[dy+y][dx+x]
            if mv1.isalpha():
                return ''.join(sorted(maze[dy+y][dx+x] + maze[2*dy+y][2*dx+x]))
        return None
    # Scan for portals
    for y, r in enumerate(maze):
        for x, c in enumerate(r):
            if c == '.':
                p = hasPortal(x, y)
                if p:
                    portalToPoints[p].append((x, y))
                    pointToPortals[(x, y)] = p

    # Just do the search, I guess
    start = portalToPoints['AA'][0]
    visited = {start}
    toVisit = [(0, start)]

    target = portalToPoints['ZZ'][0]

    def getEdges(loc):
        x, y = loc
        for dy,dx in DIRS:
            neighbor = (dx+x, dy+y)
            c = maze[neighbor[1]][neighbor[0]]
            if c == '.':
                yield neighbor
        # Check if neighbor is in a portal
        if loc in pointToPortals:
            portal = pointToPortals[loc]
            points = portalToPoints[portal]

            for p in points:
                if p != loc:
                    yield p
        

    while toVisit:
        cost, location = toVisit.pop(0)

        for n in getEdges(location):
            if n not in visited:
                costToNeighbor = cost + 1
                if n == target:
                    return costToNeighbor
                visited.add(n)
                toVisit.append((costToNeighbor, n))


def solveMazePart2(maze):
    portalToPoints = defaultdict(list)
    pointToPortals = {}

    height = len(maze)
    width = len(maze[0])

    def isOutside(p):
        x, y = p
        return y < 3 or height - y < 4 or x < 3 or width - x < 4


    def hasPortal(x, y):
        for dy,dx in DIRS:
            mv1 = maze[dy+y][dx+x]
            if mv1.isalpha():
                return ''.join(sorted(maze[dy+y][dx+x] + maze[2*dy+y][2*dx+x]))
        return None
    # Scan for portals
    for y, r in enumerate(maze):
        for x, c in enumerate(r):
            if c == '.':
                p = hasPortal(x, y)
                if p:
                    portalToPoints[p].append((x, y))
                    pointToPortals[(x, y)] = p

    # Just do the search, I guess
    start = portalToPoints['AA'][0]
    visited = {(0, start)}

    from collections import deque
    
    toVisit = deque([(0, (0, start))])

    target = (0, portalToPoints['ZZ'][0])

    def getEdges(loc):
        level, p = loc
        x, y = p
        for dy,dx in DIRS:
            neighbor = (dx+x, dy+y)
            c = maze[neighbor[1]][neighbor[0]]
            if c == '.':
                yield (level, neighbor)
        # Check if neighbor is in a portal
        if p in pointToPortals:
            portal = pointToPortals[p]
            points = portalToPoints[portal]

            if not(isOutside(p) and level == 0):
                levelDelta = -1 if isOutside(p) else 1
                for pn in points:
                    if pn != p:
                        yield (level + levelDelta, pn)
        

    while toVisit:
        cost, node = toVisit.popleft()

        for n in getEdges(node):
            if n not in visited:
                costToNeighbor = cost + 1
                if n == target:
                    return costToNeighbor
                visited.add(n)
                toVisit.append((costToNeighbor, n))


if __name__ == "__main__":
    maze = []
    with open("input_day20") as f:
        maze = list(map(list, map(lambda x: x.strip('\n').strip('\r'), f.readlines())))

    print(solveMaze(maze))
    print(solveMazePart2(maze))
