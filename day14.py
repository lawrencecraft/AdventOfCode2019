import math

MEMOIZE_ORE_LEVEL={}
# Additional ore required
def calculateOre(quantity, reactant, ingredients, waste, indent=0, loud=False):
    def iprint(msg):
        if loud:
            print("  " * indent + msg)

    iprint(f"Trying to make {quantity} {reactant}")

    if reactant == 'ORE':
        return quantity

    inWaste = waste.get(reactant, 0)
    reusedReactant = min(inWaste, quantity)
    requiredReactant = quantity - reusedReactant
    waste[reactant] = inWaste - reusedReactant

    iprint(f"We have {inWaste} already, reusing {reusedReactant}. We still have {waste[reactant]}.")
    iprint(f"Producing {requiredReactant}...")
    if requiredReactant > 0:
        perBatch, inputs = ingredients[reactant]
        batches = math.ceil(requiredReactant / perBatch)
        wastedReactant = perBatch * batches - requiredReactant
        ore = 0
        for quantity, ip in inputs:
            ore += calculateOre(quantity * batches, ip, ingredients, waste, indent=indent+1, loud=loud)

        waste[reactant] = waste.get(reactant, 0) + wastedReactant
        return ore
    else:
        return 0

def buildFuel(reactants, target, qty, loud=False):
    reactantTable = {}
    for output, inputs in reactants:
        q, nm = output
        reactantTable[nm] = (q, inputs)

    return calculateOre(qty, target, reactantTable, {}, loud=loud)

def parseInput(i):
    q, n = i.split(' ')
    return (int(q), n)

# Return an initial interval
def findTop(maxOre, reactants, root):
    lastStart = 0
    start = 1024

    while buildFuel(reactants, root, start) <= maxOre:
        lastStart = start
        start *= 2

    return lastStart, start

def binaryChopOre(maxOre, reactants, root):
    minim, maxim = findTop(maxOre, reactants, root)

    # Binary search these fools
    def works(qty):
        return buildFuel(reactants, root, qty) <= maxOre

    while minim < maxim:
        mid = (minim + maxim) // 2

        if works(mid):
            # Take top half
            minim = mid + 1
        else:
            # Take bottom half
            maxim = mid - 1
        print(minim, maxim, mid)
    return maxim


if __name__ == "__main__":
    r = []
    with open("input_day14") as f:
        for l in f.readlines():
            input_line, output = map(lambda x: x.strip(), l.split('=>'))
            inputs = list(map(parseInput, input_line.split(', ')))
            
            r.append((parseInput(output), inputs))
    # pt1
    print(buildFuel(r, 'FUEL', 1, loud=True))

    #pt2
    print(binaryChopOre(1000000000000, r, 'FUEL'))

