

def chunk(arr, size):
    i = 0
    while i < len(arr):
        yield arr[i:i+size]
        i += size

def assembleLayers(data, x, y):
    size = x * y
    layers = list(chunk(data, size))
    result = [2] * size # Everything is transparent
    for layer in layers:
        for pos, pixel in enumerate(layer):
            if result[pos] == 2:
                result[pos] = pixel
    return result

def printImage(data, x):
    m = {
        0: " ",
        1: "O"
    }
    for line in chunk(list(map(m.get, data)), x):
        print(''.join(line))







if __name__ == "__main__":
    d = None
    with open("input_day8") as f:
        d = list(int(x) for x in f.read())

    final = assembleLayers(d, 25, 6)
    printImage(final, 25)