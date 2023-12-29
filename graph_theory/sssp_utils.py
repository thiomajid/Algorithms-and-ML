"""
Defines basic data structures for representing graphs and edges used to solve
single-source shortest path problems.

Each node is represented by an integer, and each edge is represented by a tuple of
the form (tail, head, weight).

The graph is represented by a list of nodes and a list of edges.
"""


from typing import NamedTuple


class Edge(NamedTuple):
    """
    Data structure representing an edge in a directed graph.
    """

    tail: int
    head: int
    weight: int

    def __repr__(self) -> str:
        return f"Edge(tail={self.tail}, head={self.head}, weight={self.weight})"


class Graph:
    """
    A directed graph represented by a list of nodes and a list of edges.
    """

    def __init__(self, nodes: list[int], edges: list[Edge]) -> None:
        self.nodes = nodes
        self.edges = edges

    def __repr__(self) -> str:
        return f"Graph(nodes={self.nodes}, edges={self.edges})"

    def __str__(self) -> str:
        return self.__repr__()
