import networkx as nx
import numpy as np

def influence_diffusion(G: nx.Graph, S: set[int], t: np.ndarray):
    I = S
    sizes = [len(I)]
    i = 0
    while True:
        influenced = {v for v in set(G.nodes()).difference(I) if len(set(nx.neighbors(G, v)).intersection(I)) >= t[v]}
        _I = I.union(influenced)
        if _I == I:
            break
        I = _I
        sizes.append(len(I))
        i += 1
    return I, sizes, i