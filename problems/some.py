# Credit to lecture 8 and 9 regarding Network Flow
# It helped us find the appropriate algorithm for finding paths between two vertices
# Where a property must hold.
# Also looked at Algorithm Design book, Chapter 7
# Credit NetworkX

import networkx as nx
# Import manual as the api call is not in top level for nx for some reason.
from networkx.algorithms.connectivity import local_node_connectivity

# Return true if there is a path from s to t that includes at least one red vertex.
# Else return false

def some_dag(g, start_vertex, target_vertex):
    from_s = nx.descendants(g, start_vertex) | {start_vertex}
    from_t = nx.ancestors(g, target_vertex) | {target_vertex}

    # If the same red vertex is BOTH in from_s and from_t, there is a red s-t path:
    # s -> red_v -> t.
    for v in from_s & from_t:
        if g.nodes[v]["color"] == "red": return True

    return False

def some_undirected(g, start_vertex, target_vertex):
    red_vertices = set()
    for vertex, data in g.nodes(data=True):
            if data.get("color") == "red":
                red_vertices.add(vertex)
    g_ = g.copy()
    x = object()
    g_.add_node(x, color="black")
    g_.add_edges_from([(start_vertex, x), (target_vertex, x)])

    for r in red_vertices:
        # Stop after 2 augmenting paths we don't need the full max flow
        # As no auxiliary is passed it builds itself with capacity 1 for networkX 3.7
        if local_node_connectivity(g_, r, x, cutoff=2) >= 2:
            return True
    return False

def some(g, isDAG):
    start_vertex =  g.graph["start"]
    target_vertex = g.graph["target"]

    if isDAG:
        return some_dag(g, start_vertex, target_vertex)
        
    else: # Undirected
        return some_undirected(g, start_vertex, target_vertex)