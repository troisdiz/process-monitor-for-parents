from itertools import groupby


def test_pocs():

    data = [('k1', 1), ('k2', 4), ('k3', 6), ('k2', 8), ('k1', 3)]

    groups = []
    uniquekeys = []
    data = sorted(data, key=lambda t: t[0])
    for k, g in groupby(data, lambda t: t[0]):
        groups.append(list(g))  # Store group iterator as a list
        uniquekeys.append(k)
    print(groups)
    print(uniquekeys)
