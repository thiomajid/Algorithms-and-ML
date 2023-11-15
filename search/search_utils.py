from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union

TState = TypeVar("TState")


class AbstractNode(ABC, Generic[TState]):
    def __init__(
        self,
        action: str,
        state: TState,
        parent: Union[TState, None] = None,
    ) -> None:
        super().__init__()

        self.action = action
        self.state = state
        self.parent = parent

    def __repr__(self) -> str:
        return f"Node(action={self.action}, state={self.state}, parent={self.parent})"

    def __str__(self) -> str:
        return self.__repr__()


def reconstruct_path(goal: AbstractNode):
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


class AbstractFrontier(ABC, Generic[TState]):
    @abstractmethod
    def add(self, state: AbstractNode) -> None:
        pass

    @abstractmethod
    def remove(self) -> AbstractNode:
        pass

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def _has_state(self, state: TState) -> bool:
        pass


class StackFrontier(AbstractFrontier[TState]):
    def __init__(self) -> None:
        super().__init__()

        self.frontier: list[AbstractNode] = []

    def __len__(self) -> int:
        return len(self.frontier)

    def __contains__(self, __obj: object) -> bool:
        if not isinstance(__obj, AbstractNode):
            return False

        return self.has_state(__obj)

    @property
    def is_empty(self):
        return len(self) == 0

    def add(self, node: AbstractNode):
        return self.frontier.append(node)

    def remove(self):
        return self.frontier.pop()

    def _has_state(self, state: TState):
        return any(node.state == state for node in self.frontier)


class QueueFrontier(StackFrontier[TState]):
    def __init__(self) -> None:
        super().__init__()

    def remove(self):
        return self.frontier.pop(0)
