from math import ceil

def f1(S: set[int], neighbors: dict[int, set[int]]) -> float:
    result = 0
    for v, n_v in neighbors.items():
        result += min(len(n_v & S), ceil(len(n_v) / 2))
    return result
