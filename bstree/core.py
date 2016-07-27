"""
BSTree implementation

"""

__all__ = [
    'is_node',
    'new_bstree'
]


class Node:
    __slots__ = (
        '_key',
        '_value',
        '_left_child',
        '_right_child'
    )

    def __init__(self, key, value, left_child=None, right_child=None):
        self._key = key
        self._value = value
        self._left_child = left_child
        self._right_child = right_child

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __le__(self, other):
        return self.key <= other.key

    def __ge__(self, other):
        return self.key >= other.key

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def left_child(self):
        return self._left_child

    @left_child.setter
    def left_child(self, node):
        if node is not None and not is_node(node):
            raise TypeError('Value is not node')

        self._left_child = node

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, node):
        if node is not None and not is_node(node):
            raise TypeError('Value is not node')

        self._right_child = node


class BSTree:
    def __init__(self):
        self._root = None
        self._nodes_count = 0

    def get(self, key):
        current_root = self.root

        while current_root is not None:
            if key == current_root.key:
                return current_root
            elif key < current_root.key:
                current_root = current_root.left_child
            else:
                current_root = current_root.right_child

        return None

    def add(self, key, value):
        if self.root is None:
            self.root = _new_node(key, value)
            self._nodes_count += 1
            return None

        current_root = self.root

        while True:
            if key == current_root.key:
                current_root.value = value
                return None
            elif key < current_root.key:
                if current_root.left_child is None:
                    current_root.left_child = _new_node(key, value)
                    self._nodes_count += 1
                    return None

                current_root = current_root.left_child
            else:
                if current_root.right_child is None:
                    current_root.right_child = _new_node(key, value)
                    self._nodes_count += 1
                    return None

                current_root = current_root.right_child

    def remove(self, key):
        parent = None
        current_root = self.root

        while current_root is not None:
            if key == current_root.key:
                break

            parent = current_root

            if key < current_root.key:
                current_root = current_root.left_child
            else:
                current_root = current_root.right_child

        if current_root is None:
            return None

        if current_root.right_child is None:
            self._swap_node(parent, current_root, current_root.left_child)
        elif current_root.left_child is None:
            self._swap_node(parent, current_root, current_root.right_child)
        else:
            min_node = self._find_min_node(current_root)
            self._swap_node(parent, current_root, min_node)

        self._nodes_count -= 1

    def _swap_node(self, parent, current_child, new_child):
        if parent is None:
            self.root = new_child
        elif current_child is parent.left_child:
            parent.left_child = new_child
        else:
            parent.right_child = new_child

    @staticmethod
    def _find_min_node(node):
        if node is None:
            return None

        while True:
            if node.left_child is None:
                return node
            else:
                node = node.left_child

    @staticmethod
    def _find_max_node(node):
        if node is None:
            return None

        while True:
            if node.right_child is None:
                return node
            else:
                node = node.right_child

    def find_min(self):
        node = self._find_min_node(self.root)
        return node.key, node.value

    def find_max(self):
        node = self._find_max_node(self.root)
        return node.key, node.value

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, node):
        if not is_node(node):
            raise TypeError('Value is not node')

        self._root = node

    def __len__(self):
        return self._nodes_count

    def __contains__(self, item):
        if is_node(item):
            key = item.key
        else:
            key = item

        return bool(self.get(key))

    def __bool__(self):
        return bool(self.root)

    def __getitem__(self, key):
        return self.get(key).value

    def __setitem__(self, key, value):
        node = self.get(key)
        node.value = value


def _new_node(key, value, left_child=None, right_child=None):
    """
    Creates and returns new node of BSTree

    """
    return Node(key, value, left_child, right_child)


def is_node(obj):
    """
    Returns True if object is node of BSTree

    """
    return isinstance(obj, Node)


def new_bstree():
    """
    Creates and returns new BSTree

    """
    return BSTree()
