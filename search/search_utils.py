from abc import ABC, abstractmethod
from typing import Generic, NamedTuple, TypeVar, Union

from graphviz import Digraph

_TState = TypeVar("_TState")


class AbstractNode(ABC, Generic[_TState]):
    def __init__(
        self,
        action: str,
        state: _TState,
        parent: Union[_TState, None] = None,
    ) -> None:
        super().__init__()

        self.action = action
        self.state = state
        self.parent = parent

    def __repr__(self) -> str:
        return f"Node(action={self.action}, state={self.state}, parent={self.parent})"

    def __str__(self) -> str:
        return self.__repr__()


class AbstractFrontier(ABC, Generic[_TState]):
    def __init__(self) -> None:
        super().__init__()

        self.frontier: list[AbstractNode] = []

    def __len__(self):
        return len(self.frontier)

    def __contains__(self, __obj: object) -> bool:
        if not isinstance(__obj, AbstractNode):
            return False

        return self.has_state(__obj)

    @property
    def is_empty(self):
        return len(self) == 0

    @abstractmethod
    def add(self, state: AbstractNode[_TState]) -> None:
        pass

    @abstractmethod
    def remove(self) -> AbstractNode[_TState]:
        pass

    @abstractmethod
    def _has_state(self, state: _TState) -> bool:
        pass


class StackFrontier(AbstractFrontier[_TState]):
    def __init__(self) -> None:
        super().__init__()

    def add(self, node: AbstractNode[_TState]):
        return self.frontier.append(node)

    def remove(self):
        return self.frontier.pop()

    def _has_state(self, state: _TState):
        return any(node.state == state for node in self.frontier)


class QueueFrontier(StackFrontier[_TState]):
    def __init__(self) -> None:
        super().__init__()

    def remove(self):
        return self.frontier.pop(0)


class Edge(NamedTuple):
    source: AbstractNode[_TState]
    dest: AbstractNode[_TState]

    def __hash__(self) -> int:
        return hash(id(self))


def reconstruct_path(goal: AbstractNode[_TState]):
    r"""
    Reconstructs the path from the goal node to the initial node

    Args:
    -----
        goal: `AbstractNode`
            The goal node that was the objective of the search
    """
    path = [goal]
    node = goal

    # Reconstruct path from goal to initial node by following parent pointers
    while node.parent is not None:
        path.append(node.parent)
        node = node.parent

    return path[::-1]


def trace_graph(goal: AbstractNode[_TState]):
    nodes, edges = set[AbstractNode[_TState]](), set[Edge]()

    def build(v: AbstractNode[_TState]):
        if v not in nodes:
            nodes.add(v)

            if v.parent is not None:
                edges.add(Edge(source=v.parent, dest=v))
                build(v.parent)

    build(goal)

    return nodes, edges


def draw_path(goal: AbstractNode[_TState]):
    dot = Digraph(format="svg", graph_attr={"rankdir": "TB"})
    nodes, edges = trace_graph(goal)

    for node in nodes:
        uid = str(id(node))
        # for any value in the graph, create a rectangular ('record') node for it
        dot.node(name=uid, label="{ %s }" % (node.state,), shape="record")

        if node.action:
            # if this node is the result of some action, create an action node for it
            action_uid = uid + node.action
            dot.node(name=action_uid, label=node.action)

            # and connect this node to it
            dot.edge(action_uid, uid)

    for edge in edges:
        # connect node1 to the operation of node2
        dot.edge(str(id(edge.source)), str(id(edge.dest)) + edge.dest.action)

    return dot
