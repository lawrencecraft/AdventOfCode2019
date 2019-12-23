from intcode import startWithStaticInput

BOX_SIZE=99

def part1(program):
    m = [[0] * 50 for _ in range(50)]

    def setMap(x, y, p):
        m[y][x] = p

    def findBeam(x, y):
        startWithStaticInput(program, inputQueue=[
                             x, y], handleOutput=lambda p: setMap(x, y, p))
    for x in range(50):
        for y in range(50):
            findBeam(x, y)

    return sum(1 for row in m for c in row if c == 1)


def part2(program):

    def getValueAt(x, y):
        op = []
        startWithStaticInput(program, inputQueue=[
                             x, y], handleOutput=op.append)
        return op[0]

    def doesItFit(bottomLeftX, bottomLeftY):
        vertices = [
            (bottomLeftX, bottomLeftY),
            (bottomLeftX, bottomLeftY - BOX_SIZE),
            (bottomLeftX + BOX_SIZE, bottomLeftY),
            (bottomLeftX + BOX_SIZE, bottomLeftY - BOX_SIZE)
        ]

        for ex, ey in vertices:
            if not getValueAt(ex, ey):
                return False

        return True


    row = 100
    col = 100

    while True:
        v = getValueAt(col, row)
        if v and doesItFit(col, row):
            print(f"Bottom left is ({col}, {row})")
            return (col, row - BOX_SIZE)
        elif v:
            row += 1
            # print("skip")
        else:
            col += 1


if __name__ == "__main__":
    ops = []
    with open("input_day19") as f:
        ops = list(map(int, f.read().split(',')))

    #
    # print(part1(ops))
    x, y = part2(ops)
    print(x * 10000 + y)
