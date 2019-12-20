orbits = dict({tuple(reversed(o.strip().split(')'))) for o in open("input_day6").readlines()})

print(orbits)