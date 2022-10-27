import itertools
from collections.abc import Sequence


class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def flatten(node):
    result = []
    if node.left:
        result = list(itertools.chain(flatten(node.left), result))
    result.append(node)
    if node.right:
        result = list(itertools.chain(result, flatten(node.right)))
    return result


class IndexableNode(BinaryNode):
    def __str__(self):
        return f"value: {self.value}, left: [{self.left}], right: [{self.right}]"

    def __getitem__(self, index):
        found = flatten(self)[index]
        if not found:
            raise IndexError('Index out of range')
        return found.value


class SequanceNode(IndexableNode):

    def __len__(self):
        return len(flatten(self))


class CollectionNode(SequanceNode, Sequence):
    pass


if __name__ == '__main__':
    #      10
    #    /    \
    #   5      15
    #  / \     /
    # 2   6  11
    #       \
    #         7
    tree = CollectionNode(
        10,
        left=CollectionNode(5,
                            left=CollectionNode(2),
                            right=CollectionNode(
                                6, right=CollectionNode(7))),
        right=CollectionNode(15, left=CollectionNode(11))

    )

    assert tree[0] == 2
    assert tree[1] == 5
    assert list(tree) == [2, 5, 6, 7, 10, 11, 15]
    print('Tree: ', list(tree))
    print(len(tree))
    assert tree.index(7) == 3
    assert tree.count(10) == 1
