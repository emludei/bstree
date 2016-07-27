import unittest
import random

from string import ascii_letters

from bstree.core import Node, BSTree


def value_chars(length=100):
    return (random.choice(ascii_letters) for _ in range(length))


def get_list_of_nodes(count=100, start=-10000, end=10000):
    keys = set()
    result = []

    for _ in range(count):
        key = random.randint(start, end)

        if key not in keys:
            result.append((key, ''.join(value_chars())))
            keys.add(key)

    return result


class TestNode(unittest.TestCase):
    def new_node(self, start=-10000, end=1000):
        return random.randint(start, end), ''.join(value_chars())

    def new_node_key(self, node, new_key=10):
        node.key = new_key

    def test_node_properties(self, iterations=10000):
        for _ in range(iterations):
            nodes = [self.new_node() for _ in range(3)]

            left_child = Node(*nodes[0])
            right_child = Node(*nodes[1])
            parent_node = Node(*nodes[2], left_child, right_child)

            self.assertEqual(parent_node.key, nodes[2][0])
            self.assertEqual(parent_node.value, nodes[2][1])

            new_value = ''.join(value_chars())
            parent_node.value = new_value

            self.assertEqual(parent_node.value, new_value)
            self.assertNotEqual(parent_node.value, nodes[2][1])

            self.assertRaises(AttributeError, self.new_node_key, parent_node)

            self.assertIs(parent_node.left_child, left_child)
            self.assertIs(parent_node.right_child, right_child)

            new_left_child = Node(*self.new_node())
            parent_node.left_child = new_left_child

            self.assertIs(parent_node.left_child, new_left_child)
            self.assertIsNot(parent_node.left_child, left_child)

    def test_comparisons(self):
        first = self.new_node(start=-100, end=10)
        second = self.new_node(start=100, end=10000)

        self.assertGreater(second, first)
        self.assertLess(first, second)

        self.assertGreaterEqual(second, first)
        self.assertLessEqual(first, second)

        self.assertNotEqual(first, second)

        key = 100
        value = 'test'

        first = Node(key, value)
        second = Node(key, value)

        self.assertEqual(first, second)

        self.assertGreaterEqual(first, second)
        self.assertLessEqual(first, second)


class TestBSTree(unittest.TestCase):
    def test_bstree(self, iterations=100):
        for _ in range(iterations):
            nodes = get_list_of_nodes()
            sorted_nodes = sorted(nodes[:], key=lambda item: item[0])
            bstree = BSTree()

            self.assertEqual(0, len(bstree))

            bstree.remove(random.randint(0, 100))

            self.assertEqual(0, len(bstree))
            self.assertFalse(bool(bstree))

            [bstree.add(key, value) for key, value in nodes]

            self.assertEqual(bstree.find_min(), sorted_nodes[0])
            self.assertEqual(bstree.find_max(), sorted_nodes[-1])

            self.assertTrue(random.choice(nodes)[0] in bstree)

            max_key = max(nodes, key=lambda item: item[0])[0]
            self.assertFalse(random.randint(max_key, max_key + 1000) in bstree)

            node = random.choice(nodes)

            self.assertEqual(node[1], bstree[node[0]])

            new_value = ''.join(value_chars())

            bstree[node[0]] = new_value

            self.assertNotEqual(node[1], bstree[node[0]])
            self.assertEqual(new_value, bstree[node[0]])

            removed_item = nodes.pop(random.randint(0, len(nodes) - 1))

            self.assertEqual(bstree.get(removed_item[0]).key, removed_item[0])

            bstree.remove(removed_item[0])

            self.assertIsNone(bstree.get(removed_item[0]))


if __name__ == '__main__':
    unittest.main()
