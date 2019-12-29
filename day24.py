
def calculateBiodiversity(state):
    offset = 0
    biodiversity = 0
    for row in state:
        for c in row:
            if c == '#':
                biodiversity |= 1 << offset
            offset += 1
    return biodiversity


def evolve(state):
    def calcNeighbors(row, col):
        neighbors = 0
        if row > 0:
            neighbors += 1 if state[row - 1][col] == '#' else 0
        if row < len(state) - 1:
            neighbors += 1 if state[row + 1][col] == '#' else 0
        if col > 0:
            neighbors += 1 if state[row][col - 1] == '#' else 0
        if col < len(state[0]) - 1:
            neighbors += 1 if state[row][col + 1] == '#' else 0

        return neighbors

    
    newState = [[None] * len(state[0]) for _ in state]
    for i, row in enumerate(state):
        for j, c in enumerate(row):
            neighbors = calcNeighbors(i, j)
            if c == '.':
                newState[i][j] = '#' if 0 < neighbors < 3  else '.'
            elif c == '#':
                newState[i][j] = '#' if neighbors == 1 else '.'
            else:
                raise Exception("Some shizz")
    return newState

def part1(initialState):
    states = set()
    iterations = 0
    states.add(calculateBiodiversity(initialState))

    currentState = initialState
    while True:
        currentState = evolve(currentState)
        iterations += 1
        biodiv = calculateBiodiversity(currentState)
        if biodiv in states:
            return biodiv, iterations
        
        states.add(biodiv)

# def evolve2

def part2(initialState):
    currentLayer = [initialState]
    middlePoint = 2
    for _ in range(200):
        pass

if __name__ == "__main__":
    initialState = []
    with open("input_day24") as f:
        initialState = map(list, map(lambda x: x.strip(), f.readlines()))

    print(part1(initialState))
