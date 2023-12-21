from union_find import Node, find, makeset, union, delete
import unittest

class TestUnionFind(unittest.TestCase):
    def setUp(self):
        self.uf = [None] * 10
        for i in range(10):
            makeset(self.uf, i, i)

    def test_find(self):
        self.assertEqual(find(self.uf, 0).element, 0)
        union(self.uf, 0, 1)
        self.assertEqual(find(self.uf, 1).element, 0)  

    def test_union(self):
        union(self.uf, 2, 3)
        union(self.uf, 3, 4)
        self.assertEqual(find(self.uf, 4).element, 2) 

    def test_delete_leaf_node(self):
        delete(self.uf, 5)
        self.assertIsNone(self.uf[5])

    def test_delete_node_with_children(self):
        union(self.uf, 6, 7)
        union(self.uf, 7, 8)
        delete(self.uf, 7)
        self.assertIsNone(self.uf[7])  

    def test_union_chain(self):
        union(self.uf, 0, 1)
        union(self.uf, 1, 2)
        self.assertEqual(find(self.uf, 2).element, 0)

    def test_union_subsets(self):
        union(self.uf, 3, 4)
        union(self.uf, 5, 6)
        union(self.uf, 4, 6)
        self.assertEqual(find(self.uf, 6).element, 3)

    def test_create_sets_with_different_elements(self):
        uf_strings = [None] * 5
        makeset(uf_strings, 0, "apple")
        makeset(uf_strings, 1, "orange")
        makeset(uf_strings, 2, "banana")
        union(uf_strings, 0, 1)
        union(uf_strings, 2, 1)
        self.assertEqual(find(uf_strings, 1).element, "apple")

    def test_delete_last_node(self):
        uf_single_node = [None]
        makeset(uf_single_node, 0, 42)
        delete(uf_single_node, 0)
        self.assertIsNone(uf_single_node[0])

if __name__ == '__main__':
    unittest.main()
