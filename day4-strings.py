NUM_RANGE = range(357253, 892942)

print(sum(1 for s in map(str, NUM_RANGE) if list(s) == sorted(s) and len(set(s)) != len(s)))
print(sum(1 for s in map(str, NUM_RANGE) if list(s) == sorted(s) and 2 in map(s.count, s)))