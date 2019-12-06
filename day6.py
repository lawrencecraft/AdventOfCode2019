
def loadOrbits():
    with open("input_day6") as f:
        return [o.split(')') for o in f.readlines()] 

def solveIt(orbits):
    print(len(orbits))

if __name__ == "__main__":
    orbits = loadOrbits()
    solveIt(orbits)