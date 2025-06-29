from math import ceil
import networkx as nx

def uniform_cost() -> float:
    def wrapper(n: int, G: nx.Graph):
        return 1
    return wrapper

def degree_cost(degrees: dict) -> float:
    def wrapper(n: int, G: nx.Graph):
        return ceil(degrees[n] / 2)
    return wrapper

