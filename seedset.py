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
            if sum([c(n, G) for n in S_p]) > k:
                break
            S_d = S_p
        # Now S_d is a set of nodes that can be selected
        return S_d, k
    return wrapper

from copy import deepcopy

# def worker(G, S_d, v, f, c, neighbors):
#     return (f(S_d.union({v}), neighbors) - f(S_d, neighbors)) / c(v, G)

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

from math import ceil, log2

def purp(G: nx.Graph, c: callable, d: int):
    V = set(G.nodes())
    def wrapper(k: int):
        i = 0
        S = set()
        ss_cost = 0
        _G = nx.Graph(nx.subgraph(G, V)) # Induced subgraph
        while True:
            i += 1
            print(f"Iteration {i}, S: {len(S)} k: {k}")
            betweenness = nx.betweenness_centrality(_G, ceil(log2(G.number_of_nodes()))) # Calculate betweenness centrality
            betweenness = np.array([betweenness[v] if v in betweenness else -1 for v in range(max(G.nodes()) + 1)])
            # Get the node with maximum betweenness centrality
            candidates = np.argsort(-betweenness)[:d]
            for u in candidates:
                # Check the cost
                u_cost = c(u, G)
                if ss_cost + u_cost > k:
                    _G.remove_node(u)
                    continue
                S.add(u)
                ss_cost += u_cost
                # Remove the node from the graph
                _G.remove_node(u)
            if ss_cost >= k or len(_G.nodes()) == 0:
                break
        return S, ss_cost
    return wrapper
