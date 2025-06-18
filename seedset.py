import networkx as nx

# Random Seeds Selection

from random import randint

def random_seeds(G: nx.Graph, c: callable) -> set[int]:
    def wrapper(k: int):
        S_p = set()
        S_d = set()
        while True:
            # Add a random node to S_p
            S_p.add(randint(0, G.number_of_nodes() - 1))
            if sum([c(n, G) for n in S_p]) >= k:
                break
            S_d = S_p
        # Now S_d is a set of nodes that can be selected
        return S_d, k
    return wrapper

# Cost-based Greedy Algorithm

from multiprocessing import Pool
from copy import deepcopy

def worker(G, S_d, v, f, c, neighbors):
    return (f(S_d.union({v}), neighbors) - f(S_d, neighbors)) / c(v, G)

def cost_seeds_greedy(G: nx.Graph, c: callable, f: callable) -> tuple[set[int], float]:
    def wrapper(k: int):
        S_p = set()
        S_d = set()
        nodes = set(G.nodes())
        neighbors = {n: set(G.neighbors(n)) for n in nodes}

        while True:
            nodes = list(nodes.difference(S_d))
            with Pool(24) as pool:
                candidates = pool.starmap(worker, [(G, S_d, v, f, c, neighbors) for v in nodes])
            u = nodes[candidates.index(max(candidates))]
            S_p = deepcopy(S_d)
            S_d = S_p.union({u})
            if sum([c(n, G) for n in S_d]) > k:
                break
            nodes = set(nodes)
        return S_p, sum([c(n, G) for n in S_p])
    return wrapper

# WTSS

import numpy as np

def wtss(G: nx.Graph, c: callable, t: np.ndarray):
    def wrapper(k: int):
        S = set()
        _G = deepcopy(G)
        d = np.array(list(dict(nx.degree(G)).values()))
        _t = t.copy()
        while len(_G.nodes()) > 0:
            activated = [i for i in (t == 0).nonzero()[0].tolist() if i in _G.nodes()]
            candidates = [i for i in (d < t).nonzero()[0].tolist() if i in _G.nodes()]
            if len(activated) > 0:
                v = activated[0]
                for u in nx.neighbors(_G, v):
                    _t[u] = max(_t[u] - 1, 0)
            elif len(candidates) > 0:
                v = candidates[0]
                # Check the costs
                if sum([c(n, _G) for n in S]) + c(v, _G) > k:
                    break
                S.add(v)
                for u in nx.neighbors(_G, v):
                    _t[u] = _t[u] - 1
            else:
                candidates = {
                    u: (c(u, _G) * t[u])/(d[u] * (d[u] + 1))
                    for u in _G.nodes()
                }
                v = max(candidates, key=candidates.get)
            for u in nx.neighbors(_G, v):
                d[u] = d[u] - 1
            _G.remove_node(v)
        return S, sum([c(n, G) for n in S])
    return wrapper
