"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy
import copy

def print_list(l):
    for i in l:
        print(i)

def riffle(ll):
    """ Take a list of lists and riffle them """
    ret = []

    maxlen = max(map(len, ll))

    i = 0
    
    while i < maxlen:
        for l in ll:
            if len(l) > i:
                ret.append(l[i])
        i += 1

    return ret

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

    def bft_recursive(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        def remove_from_graph(node, graph):
            if node in graph:
                del graph[node]
                for i in graph:
                    if node in graph[i]:
                        graph[i].remove(node)
            
            return graph

        def bft(queue, graph):
            if queue.size() == 0:
                return []

            node = queue.dequeue()

            if node in graph:
                # Get node context
                neigh = graph[node]
                if node in neigh:
                    neigh.remove(node)
                neigh = list(neigh)

                # Get subgraph without node
                g = remove_from_graph(node, graph)

                # Add neighborhood to the end of the queue,
                # so it's searched after those currently queued.
                queue.enqueue_list(neigh)

                # Prepend node to front of search.
                return [node] + bft(queue, g)
            else:
                return bft(queue, graph)
        
        starting_queue = Queue()
        starting_queue.enqueue(starting_vertex)
        out = bft(starting_queue, self.vertices.copy())

        print_list(out)

        return out

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

        def remove_from_graph(node, graph):
            if node in graph:
                del graph[node]
                for i in graph:
                    if node in graph[i]:
                        graph[i].remove(node)
            
            return graph

        def dft(stack, graph):
            if stack.size() == 0:
                return []

            node = stack.pop()

            if node in graph:
                # Get node context
                neigh = graph[node]
                if node in neigh:
                    neigh.remove(node)
                neigh = list(neigh)
                
                # Get subgraph without node
                g = remove_from_graph(node, graph)

                # Prepend neighborhood to stack so it's searched
                # before anything else.
                stack.push_list(neigh)

                # Prepend node to front of search.
                return [node] + dft(stack, g)
            else:
                return dft(stack, graph)
        
        starting_stack = Stack()
        starting_stack.push(current_vertex)
        out = dft(starting_stack, self.vertices.copy())

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

    def bfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.

        This should be done using recursion.
        """
        def remove_from_graph(node, graph):
            graphp = copy.deepcopy(graph)
            if node in graphp:
                del graphp[node]
                for i in graphp:
                    if node in graphp[i]:
                        graphp[i].remove(node)
            
            return graphp

        def bfs(options, goal):
            """ Options consists of pairs of paths with remaining graphs """

            # If there are no options left, fail.
            if options == []:
                return None

            success_options = [ p for p, g in options if p[-1] == goal ]

            # If we've found a path, return it.
            if success_options != []:
                return success_options[0]

            new_options = []
            for path, graph in options:
                node = path[-1]

                # Get context of path ending node.
                neigh = graph[node]
                if node in neigh:
                    neigh.remove(node)
                neigh = list(neigh)

                # For each thing in the neighborhood, create a new,
                # optional path with the remaining, unexplored graph.
                new_options += [ (path + [n], remove_from_graph(node, graph)) for n in neigh ]

            return bfs(new_options, goal)
        
        return bfs([([starting_vertex], self.vertices.copy())], destination_vertex)

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
            graphp = copy.deepcopy(graph)
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

                # If we've reached a dead-end, fail.
                if neigh == []:
                    return None

                # Get smaller graph
                g = remove_from_graph(node, graph)

                # Get possible search branches
                for n in neigh:
                    br = dfs(n, goal, g)
                    if br != None:
                        return [node] + br

                # Search failed.
                return None
            else:
                return None
        
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
