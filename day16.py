import itertools

BASE_PATTERN=(0, 1, 0, -1)

def patternForStep(stepNum):
    def genPattern():
        for p in BASE_PATTERN:
            for _ in range(stepNum+1):
                yield p
    return itertools.islice(itertools.cycle(genPattern()), 1, None)

def doRound(ip):
    output = []

    for step in range(len(ip)):
        pattern = patternForStep(step)
        value = abs(sum(map(lambda x: x[0] * x[1], zip(pattern, ip)))) % 10
        output.append(value)

    return output

def doFakeRounds(d):
    for _ in range(100):
        cumsum = 0
        for i in range(len(d) - 1, -1, -1):
            cumsum = d[i] + cumsum
            d[i] = abs(cumsum) % 10

if __name__ == "__main__":
    signal = []
    with open("input_day16") as f:
        signal = list(map(int, f.read()))

    #for i in range(100):
    #    signal = doRound(signal)
    #print(''.join(map(str, signal[:8])))

    offset = int(''.join(map(str, signal[:7])))
    data = (signal * 10000)[offset:]

    print(offset)
    print(len(signal) * 10000- offset)
    doFakeRounds(data)
    print(data[:8])
