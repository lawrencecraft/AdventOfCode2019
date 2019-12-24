def loadInstructions():
    with open("input_day22") as f:
        return [x.strip() for x in f.readlines()]

def part1(instructions, deck, pos):
    
    for i in instructions:
        if i.startswith("cut "):
            num = int(i[4:])
            pos = (pos - num) % deck
        elif i == "deal into new stack":
            pos = deck - pos - 1
        elif i.startswith("deal with increment "):
            num = int(i[len("deal with increment "):])
            pos = (num * pos) % deck
        else:
            raise Exception(f"Unknown instruction: {i}")

    return pos

def part2(instructions):
    deck = 119315717514047
    for i in reversed(instructions):
        if i.startswith("cut "):
            num = int(i[4:])
            pos = (pos - num) % deck
        elif i == "deal into new stack":
            pos = deck - pos - 1
        elif i.startswith("deal with increment "):
            num = int(i[len("deal with increment "):])
            pos = (num * pos) % deck
        else:
            raise Exception(f"Unknown instruction: {i}")


if __name__ == "__main__":
    instructions = loadInstructions()
    print(part1(instructions, 10007, 2019))
    # print(part2(instructions))
