"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

def print_list(l):
    for i in l:
        print(i)

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

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        seen = []
        
        waiting_nodes = [starting_vertex]
        while waiting_nodes != []:
            for v in waiting_nodes.copy():
                seen.append(v)
                waiting_nodes.pop(0)
                waiting_nodes += [ n for n in self.get_neighbors(v)
                                    if n not in seen and n not in waiting_nodes ]

        print_list(seen)
        return seen

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        waiting_nodes = [starting_vertex]
        i = 0
        while i < len(waiting_nodes):
            new_waiting_nodes = waiting_nodes[:i+1].copy()
            new_waiting_nodes += [ v for v in self.get_neighbors(waiting_nodes[i])
                                   if v not in new_waiting_nodes]
            new_waiting_nodes += [ w for w in waiting_nodes[i+1:] if w not in new_waiting_nodes ]
            waiting_nodes = new_waiting_nodes
            i += 1
            
        print_list(waiting_nodes)
        return waiting_nodes

    def dft_recursive(self, current_vertex):
        """
        Print each vertex in depth-first order
        beginning from a starting vertex.

        This should be done using recursion.
        """
        # if need_to_visit is None:
            # need_to_visit = set(self.vertices.keys())

        # if current_vertex in need_to_visit:
            # next_vertices = self.get_neighbors(current_vertex)
            # need_to_visit.remove(current_vertex)
        # else:
            # return []

        # return [current_vertex] + [ n for v in next_vertices
                                       # for n in self.dft_recursive(v, need_to_visit) ]

        def remove_from_graph(node, graph):
            if node in graph:
                del graph[node]
                for i in graph:
                    if node in graph[i]:
                        graph[i].remove(node)
            
            return graph

        def dft(nodes, graph):
            if nodes == []:
                return []
            elif nodes[0] in graph:
                neigh = graph[nodes[0]]
                if nodes[0] in neigh:
                    neigh.remove(nodes[0])
                g = remove_from_graph(nodes[0], graph)
                return [nodes[0]] + dft(list(neigh) + nodes[1:], g)
            else:
                return dft(nodes[1:], graph)
        
        out = dft([current_vertex], self.vertices.copy())

        print_list(out)

        return out

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        seen = {starting_vertex}

        potential_paths = [[starting_vertex]]

        while potential_paths != [] and destination_vertex not in {p[-1] for p in potential_paths}:
            potential_paths = [ p + [e] for p in potential_paths
                                        for e in self.get_neighbors(p[-1])
                                        if e not in seen ]
            seen = seen.union({p[-1] for p in potential_paths})

        if potential_paths == []:
            return None

        return [ p for p in potential_paths if p[-1] == destination_vertex ][0]

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        exhausted = {starting_vertex}

        potential_path = [starting_vertex]

        while potential_path != [] and potential_path[-1] != destination_vertex:
            next_vertices = [ v for v in self.get_neighbors(potential_path[-1])
                                if v not in potential_path and v not in exhausted ]
            if next_vertices == []:
                exhausted.add(potential_path[-1])
                potential_path.pop()
            else:
                potential_path.append(next_vertices[0])

        if potential_path == []:
            return None

        return potential_path
            

    def dfs_recursive(self, current_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        def remove_from_graph(node, graph):
            graphp = graph.copy()
            if node in graphp:
                del graphp[node]
                for i in graphp:
                    if node in graphp[i]:
                        graphp[i].remove(node)
            
            return graphp

        def dfs(node, goal, graph):
            if node == goal:
                return [node]
            elif node in graph:
                # Get list of neighbors
                neigh = graph[node]
                if node in neigh:
                    neigh.remove(node)
                neigh = list(neigh)
                if neigh == []:
                    return []

                # Get smaller graph
                g = remove_from_graph(node, graph)

                # Get possible search branches
                for n in neigh:
                    br = dfs(n, goal, g)
                    if br != []:
                        return [node] + br

                # Search failed.
                return []
            else:
                return []
        
        return dfs(current_vertex, destination_vertex, self.vertices.copy())
        

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
