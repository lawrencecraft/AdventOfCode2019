def testNum(n):
    last = None
    hasDubbadub = False
    while n > 0:
        current = n % 10
        if last is not None:
            if last < current:
                return False
            if not hasDubbadub and last == current:
                hasDubbadub = True
        last = current
        n = n // 10
    return hasDubbadub

if __name__ == "__main__":
    print(sum(1 for i in range(357253, 892942) if testNum(i)))
