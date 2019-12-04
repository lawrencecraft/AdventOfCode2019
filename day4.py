def testNum(n):
    last = None
    currentStreak = 1
    hasDubbadub = False
    while n > 0:
        current = n % 10
        if last is not None:
            if last < current:
                return False
            if last == current:
                currentStreak += 1
            else:
                hasDubbadub = hasDubbadub or currentStreak == 2
                currentStreak = 1

        last = current
        n = n // 10
    return hasDubbadub or currentStreak == 2

if __name__ == "__main__":
    print(sum(1 for i in range(357253, 892942) if testNum(i)))
