def calculateGravity(p1, p2):
    def calc(x):
        i,j = x
        if i == j:
            return 0
        elif i > j:
            return -1
        else:
            return 1
    return tuple(map(calc, zip(p1, p2)))

def calculatePlanetGravities(planets):
    velocityChanges = [tuple(0 for _ in i) for i in planets]
    for i1, p1 in enumerate(planets):
        for basei2, p2 in enumerate(planets[i1+1:]):
            i2 = basei2 + i1 + 1
            gravity = calculateGravity(p1, p2)
            def app(i, v):
                velocityChanges[i] = tuple(map(sum, zip(velocityChanges[i], v)))
            app(i1, gravity)
            app(i2, map(lambda x: -x, gravity))

    return velocityChanges

def energy(p, v):
    potential = sum(map(abs, p))
    kinetic = sum(map(abs, v))
    return potential * kinetic

def runSimulation(startingPositions, iterations = 10):
    positions = startingPositions
    velocities = [(0, 0, 0) for _ in startingPositions]

    def addLists(l1, l2):
        return [tuple(map(sum, zip(*vs))) for vs in zip(l1, l2)]
    
    for step in range(iterations):
        # Calculate gravity
        velocityChanges = calculatePlanetGravities(positions)
        velocities = addLists(velocityChanges, velocities)
        # Update positions
        positions = addLists(positions, velocities)
        
    e = sum(energy(p, v) for p, v in zip(positions, velocities))
    print(f"Energy: {e}")

def findMatch(startingPositions):
    positions = startingPositions
    print(startingPositions)
    startingVelocities = [tuple(0 for _ in p) for p in startingPositions]
    velocities = startingVelocities.copy()

    def addLists(l1, l2):
        return [tuple(map(sum, zip(*vs))) for vs in zip(l1, l2)]

    iters = 0
    
    while True:
        iters += 1
        # Calculate gravity
        velocityChanges = calculatePlanetGravities(positions)
        velocities = addLists(velocityChanges, velocities)
        # Update positions
        positions = addLists(positions, velocities)
        # print(velocities)
        # print(startingVelocities)

        if positions == startingPositions and velocities == startingVelocities:
            return iters


if __name__ == "__main__":
    positions = []
    with open("input_day12") as f:
        for l in f.readlines():
            positions.append(tuple(map(int, l.split(','))))
    # p1
    runSimulation(positions)

    items = []
    total = 1
    for i in range(3):
       m = findMatch(list(map(lambda x: (x[i],), positions)))
       print(m)
       total *= m
    print(total)
    