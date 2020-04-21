from kanren import run, eq, var, lall, lany, Relation, fact, facts

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 not in self.vertices:
            self.add_vertex(v1)

        if v2 not in self.vertices:
            self.add_vertex(v2)

        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]


class AncestorTree():

    """
    Represents a tree of ancestors from a child.
    Also keeps track of maximum depth to make finding oldest ancestor easy.
    """
    def __init__(self, node, depth = 0, parent_trees = None):
        self.node = node
        self.depth = depth
        if parent_trees is None:
            self.parent_trees = []
        else:
            self.parent_trees = parent_trees

    def add_node(self, parent_node, child_node):
        """
        Try adding a new parent to the tree.
        Returns pair of booleans;
            * if the parent was added at all
            * if the depth increased
        """

        # Get current max depth for later comparison
        if self.parent_trees != []:
            max_depth = max({ t.depth for t in self.parent_trees })
        else:
            max_depth = 0

        # If we're at the child node, try adding parent.
        if child_node == self.node:
            # If there are no current parents, add the new one and increase depth.
            if self.parent_trees == []:
                self.parent_trees.append(AncestorTree(parent_node))
                self.depth += 1
                return True, True

            # If the parent isn't present, add it.
            if parent_node not in [ t.node for t in self.parent_trees ]:
                self.parent_trees.append(AncestorTree(parent_node))
                return True, False

        # If there are no more parents to look at, fail at adding.
        if self.parent_trees == []:
            return False, False

        # Recurse to parent nodes, trying to add the new node.
        for t in self.parent_trees:
            added_Q, depth_inc = t.add_node(parent_node, child_node)
            if added_Q:
                # If a subtree of maximum depth increases, the whole depth does.
                if depth_inc and t.depth > max_depth:
                    self.depth += 1
                return added_Q, depth_inc

        # If everything fails, then adding is failed.
        return False, False

    def deepest_nodes(self):
        """ Return a set of deepest nodes """
        if self.parent_trees == []:
            return {self.node}

        max_depth = max({ t.depth for t in self.parent_trees })

        return { n for t in self.parent_trees
                   for n in t.deepest_nodes()
                   if t.depth == max_depth }


def earliest_ancestor(ancestors, starting_node):
    a_graph = Graph()
    for p, c in ancestors:
        a_graph.add_edge(c, p)

    if a_graph.get_neighbors(starting_node) == set():
        return -1

    a_tree = AncestorTree(starting_node)
    stack = [starting_node]

    while stack != []:
        node = stack.pop()
        new_nodes = list(a_graph.get_neighbors(node))
        # Make sure lowest number ancestor is returned first.
        stack += new_nodes
        for n in new_nodes:
            a_tree.add_node(n, node)

    return min(a_tree.deepest_nodes())
