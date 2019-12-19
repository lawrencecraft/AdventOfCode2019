import sys

from intcode import resumeWithInput, startNew

def rotate(current, right=True):
    x,y = current
    s = -1 if right else 1
    return (-y*s,s*x)

def paint(program):
    colors = {(0,0):1}
    
    currentPosition = (0, 0)
    currentVelocity = (0, 1)
    output = []
    state = startNew(program, lambda x: output.append(x))
    while state:
        state = resumeWithInput(state, colors.get(currentPosition, 0))
        color, direction = output

        output = []
        colors[currentPosition] = color
        currentVelocity = rotate(currentVelocity, right=direction)

        x,y=currentPosition
        dx,dy = currentVelocity
        currentPosition = (x + dx, y + dy)

    coords = colors.keys()
    xs = list(map(lambda x: x[0], coords))
    ys = list(map(lambda x: x[1], coords))
    maxx = (max(xs))
    maxy = (max(ys))
    minx = (min(xs))
    miny = (min(ys))

    for y in range(maxy, miny-1,-1):
        row = ['#' if colors.get((x, y)) == 1 else ' ' for x in range(minx, maxx+1)]
        print(''.join(row))


def doIt():
    ops = []
    with open("input_day11") as f:
        ops = list(map(int, f.read().split(',')))

    paint(ops)


if __name__ == "__main__":
    doIt()
