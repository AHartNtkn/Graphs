import unittest
import sys
import io
from graph import Graph
import copy

class Test(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_vertex(3)
        self.graph.add_vertex(4)
        self.graph.add_vertex(5)
        self.graph.add_vertex(6)
        self.graph.add_vertex(7)
        
        self.graph.add_edge(5, 3)
        self.graph.add_edge(6, 3)
        self.graph.add_edge(7, 1)
        self.graph.add_edge(4, 7)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(7, 6)
        self.graph.add_edge(2, 4)
        self.graph.add_edge(3, 5)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(4, 6)

    def test_vertices(self):
        vertices = {
          1: {2},
          2: {3, 4},
          3: {5},
          4: {6, 7}, 
          5: {3},
          6: {3},
          7: {1, 6}
        }
        self.assertDictEqual(self.graph.vertices, vertices)

    def test_bft(self):
        bft = [
            "1\n2\n3\n4\n5\n6\n7\n",
            "1\n2\n3\n4\n5\n7\n6\n",
            "1\n2\n3\n4\n6\n7\n5\n",
            "1\n2\n3\n4\n6\n5\n7\n",
            "1\n2\n3\n4\n7\n6\n5\n",
            "1\n2\n3\n4\n7\n5\n6\n",
            "1\n2\n4\n3\n5\n6\n7\n",
            "1\n2\n4\n3\n5\n7\n6\n",
            "1\n2\n4\n3\n6\n7\n5\n",
            "1\n2\n4\n3\n6\n5\n7\n",
            "1\n2\n4\n3\n7\n6\n5\n",
            "1\n2\n4\n3\n7\n5\n6\n"
        ]

        stdout_ = sys.stdout
        sys.stdout = io.StringIO()
        self.graph.bft(1)
        output = sys.stdout.getvalue()

        self.assertIn(output, bft)

        sys.stdout = stdout_  # Restore stdout

    def test_bft_recursive(self):
        bft = [
            "1\n2\n3\n4\n5\n6\n7\n",
            "1\n2\n3\n4\n5\n7\n6\n",
            "1\n2\n3\n4\n6\n7\n5\n",
            "1\n2\n3\n4\n6\n5\n7\n",
            "1\n2\n3\n4\n7\n6\n5\n",
            "1\n2\n3\n4\n7\n5\n6\n",
            "1\n2\n4\n3\n5\n6\n7\n",
            "1\n2\n4\n3\n5\n7\n6\n",
            "1\n2\n4\n3\n6\n7\n5\n",
            "1\n2\n4\n3\n6\n5\n7\n",
            "1\n2\n4\n3\n7\n6\n5\n",
            "1\n2\n4\n3\n7\n5\n6\n"
        ]

        stdout_ = sys.stdout
        sys.stdout = io.StringIO()
        self.graph.bft_recursive(1)
        output = sys.stdout.getvalue()

        self.assertIn(output, bft)

        sys.stdout = stdout_  # Restore stdout

    def test_dft(self):
        dft = [
            "1\n2\n3\n5\n4\n6\n7\n",
            "1\n2\n3\n5\n4\n7\n6\n",
            "1\n2\n4\n7\n6\n3\n5\n",
            "1\n2\n4\n6\n3\n5\n7\n"
        ]

        stdout_ = sys.stdout
        sys.stdout = io.StringIO()
        self.graph.dft(1)
        output = sys.stdout.getvalue()

        self.assertIn(output, dft)

        sys.stdout = stdout_  # Restore stdout

    def test_dft_recursive(self):
        dft = [
            "1\n2\n3\n5\n4\n6\n7\n",
            "1\n2\n3\n5\n4\n7\n6\n",
            "1\n2\n4\n7\n6\n3\n5\n",
            "1\n2\n4\n6\n3\n5\n7\n"
        ]

        stdout_ = sys.stdout
        sys.stdout = io.StringIO()
        self.graph.dft_recursive(1)
        output = sys.stdout.getvalue()

        self.assertIn(output, dft)

        sys.stdout = stdout_  # Restore stdout

    def test_bfs(self):
        old_vertices = copy.deepcopy(self.graph.vertices)

        bfs = [1, 2, 4, 6]
        self.assertListEqual(self.graph.bfs(1, 6), bfs)

        self.assertEqual(old_vertices, self.graph.vertices)
        old_vertices2 = self.graph.vertices.copy()
        
        bfs2 = [7, 6, 3, 5]
        self.assertListEqual(self.graph.bfs(7, 5), bfs2)

        self.assertEqual(old_vertices2, self.graph.vertices)

    def test_bfs_recursive(self):
        old_vertices = copy.deepcopy(self.graph.vertices)

        bfs = [1, 2, 4, 6]
        self.assertListEqual(self.graph.bfs_recursive(1, 6), bfs)

        self.assertEqual(old_vertices, self.graph.vertices)
        old_vertices2 = self.graph.vertices.copy()

        bfs2 = [7, 6, 3, 5]
        self.assertListEqual(self.graph.bfs_recursive(7, 5), bfs2)

        self.assertEqual(old_vertices2, self.graph.vertices)

    def test_dfs(self):
        dfs = [
            [1, 2, 4, 6],
            [1, 2, 4, 7, 6]
        ]
        self.assertIn(self.graph.dfs(1,6), dfs)

    def test_dfs_recursive(self):
        dfs = [
            [1, 2, 4, 6],
            [1, 2, 4, 7, 6]
        ]
        self.assertIn(self.graph.dfs_recursive(1,6), dfs)

if __name__ == '__main__':
    unittest.main()
