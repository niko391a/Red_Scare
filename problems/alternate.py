# Credit to KampJN as we repurposed her BFS to fit alternate

# Return true if there is a path from s to t that alternates between red and non-red vertices
# Else, return false

# Implement BFS and modify vertex behaviour such that you only choose vertices that has a different color to current vertex.

import networkx as nx
from collections import deque

# target_vertex['color'] == 'red'

def alternate(g):
    start_vertex =  g.graph["start"]
    target_vertex = g.graph["target"]

    # For graphs where the start and target is the same vertex
    if start_vertex == target_vertex: return True

    visited = set() # To keep track of the visited nodes in the graph
    # Add start_vertex to the list of visited nodes, s has no parent
    visited.add(start_vertex) 
    
    # Make the queue of vertices
    q = deque()
    q.append(start_vertex)


    while q:
        current_vertex = q.popleft() # Get first element

        for neighbor in g.neighbors(current_vertex):
            if neighbor not in visited and (g.nodes[neighbor]['color'] != g.nodes[current_vertex]['color']):
                visited.add(neighbor)
                q.append(neighbor)

                if neighbor == target_vertex: #If v is equal to the target node 
                    return True

    return False # the queue is empty and the function is still going, then no path has been found

