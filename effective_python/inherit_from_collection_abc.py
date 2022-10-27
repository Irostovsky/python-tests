import itertools


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


if __name__ == '__main__':
    tree = IndexableNode(10)
    assert list(tree) == [10]

    tree = IndexableNode(10,
                         left=IndexableNode(5))
    assert list(tree) == [5, 10]

    tree = IndexableNode(10,
                         left=IndexableNode(5),
                         right=IndexableNode(15))
    assert list(tree) == [5, 10, 15]

    tree = IndexableNode(10,
                         left=IndexableNode(5,
                                            left=IndexableNode(2)),
                         right=IndexableNode(15))
    assert list(tree) == [2, 5, 10, 15]

    #      10
    #    /    \
    #   5      15
    #  / \     /
    # 2   6  11
    #       \
    #         7
    tree = IndexableNode(
        10,
        left=IndexableNode(5,
                           left=IndexableNode(2),
                           right=IndexableNode(
                               6, right=IndexableNode(7))),
        right=IndexableNode(15, left=IndexableNode(11))

    )

    assert tree[0] == 2
    assert tree[1] == 5
    assert list(tree) == [2, 5, 6, 7, 10, 11, 15]
    print('Tree: ', list(tree))
    print(len(tree))
