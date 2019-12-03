
OPCODE_ADD = 1
OPCODE_MUL = 2
OPCODE_HCF = 99

def executeInstruction(index, programSpace, transform):
    src1, src2, dst = programSpace[index + 1:index + 4]
    programSpace[dst] = transform(programSpace[src1], programSpace[src2])


def processInstruction(index, programSpace) -> bool:
    opcode = programSpace[index]
    if opcode == OPCODE_ADD:
        executeInstruction(index, programSpace, lambda x, y: x + y)
        return False
    elif opcode == OPCODE_MUL:
        executeInstruction(index, programSpace, lambda x, y: x * y)
        return False
    elif opcode == OPCODE_HCF:
        return True
    else:
        raise Exception(f"Unknown opcode: {opcode}")



def runProgram(initialRam, input1, input2) -> int:
    programSpace = initialRam.copy()
    programSpace[1] = input1
    programSpace[2] = input2

    for currentInstruction in range(0, len(programSpace), 4):
        if processInstruction(currentInstruction, programSpace):
            break
    return programSpace[0]


def doIt():
    ops = []
    with open("input") as f:
        ops = list(map(int, f.read().split(',')))

    for input1 in range(0, 100):
        for input2 in range(0, 100):
            if runProgram(ops, input1, input2) == 19690720:
                print(f"Inputs: {input1}, {input2}")
                print(f"{input1 * 100 + input2}")
    



if __name__ == "__main__":
    doIt()