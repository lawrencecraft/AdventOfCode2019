from intcode import loadProgram, startNew, resumeWithInput


def part1(program):
    totalElements = 50
    outputQueues = [[] for _ in range(totalElements)]
    incomingQueues = [[] for _ in range(totalElements)]
    specialOne = None

    def generateHandler(i):
        return lambda x: outputQueues[i].append(x)

    def distributeQueues(i):
        outputQueue = outputQueues[i]
        while outputQueue:
            address = outputQueue.pop(0)
            x = outputQueue.pop(0)
            y = outputQueue.pop(0)

            if address == 255:
                return (x, y)
            else:
                incomingQueues[address].append((x, y))
                return None

    computers = [startNew(program, generateHandler(i))
                 for i in range(totalElements)]

    for i, c in enumerate(computers):
        computers[i] = resumeWithInput(c, i)
        distributeQueues(i)

    while not specialOne:
        for i, c in enumerate(computers):
            if incomingQueues[i]:
                while incomingQueues[i]:
                    x, y = incomingQueues[i].pop(0)
                    gotX = resumeWithInput(c, x)
                    computers[i] = resumeWithInput(gotX, y)
            else:
                computers[i] = resumeWithInput(c, -1)

            special = distributeQueues(i)
            if special:
                return special


def part2(program):
    totalElements = 50
    outputQueues = [[] for _ in range(totalElements)]
    incomingQueues = [[] for _ in range(totalElements)]
    natValue = None
    natSeen = set()

    def generateHandler(i):
        return lambda x: outputQueues[i].append(x)

    def distributeQueues(i):
        outputQueue = outputQueues[i]
        while outputQueue:
            address = outputQueue.pop(0)
            x = outputQueue.pop(0)
            y = outputQueue.pop(0)

            if address == 255:
                return (x, y)
            else:
                incomingQueues[address].append((x, y))
                return None

    computers = [startNew(program, generateHandler(i))
                 for i in range(totalElements)]

    for i, c in enumerate(computers):
        computers[i] = resumeWithInput(c, i)
        distributeQueues(i)

    while True:
        idleCount = 0

        for i, c in enumerate(computers):
            if incomingQueues[i]:
                while incomingQueues[i]:
                    x, y = incomingQueues[i].pop(0)
                    gotX = resumeWithInput(c, x)
                    computers[i] = resumeWithInput(gotX, y)
            else:
                idleCount += 1
                computers[i] = resumeWithInput(c, -1)

            nextNat = distributeQueues(i)
            if nextNat:
                natValue = nextNat

        if idleCount == totalElements and not sum(1 for i in incomingQueues if i):
            # All things are idle and nothing's incoming. Kick it in the trousers.
            if natValue in natSeen:
                return natValue
            incomingQueues[0].append(natValue)
            natSeen.add(natValue)



if __name__ == "__main__":
    program = loadProgram("input_day23")
    print(part1(program))
    print(part2(program))
