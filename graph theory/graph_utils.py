from collections import UserList
from typing import Generic, TypeVar

TValue = TypeVar("TValue", covariant=True)


class ListNode(Generic[TValue]):
    def __init__(self, value: TValue) -> None:
        self.value = value
        self.next: ListNode[TValue] = None


class LinkedList(Generic[TValue]):
    def __init__(self, head: ListNode) -> None:
        self._head = head

    def __iter__(self):
        try:
            node = self._head
            while node:
                yield node.value
                node = node.next
        except AttributeError:
            raise StopIteration

    def __len__(self):
        return len(list(iter(self)))

    def __repr__(self):
        return str(list(iter(self)))

    def __str__(self):
        return self.__repr__()

    @property
    def head(self):
        return self._head

    def append(self, value: TValue):
        node = self._head
        while node.next:
            node = node.next
        node.next = ListNode(value)
