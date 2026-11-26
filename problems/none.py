import networkx as nx
# https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html

def none(g):
# Needs to take the vertices from the redset and remove them from the graphs, vertices. Then run BFS
# If it not possible -1 if it is possible the length of the pass.
    # Idea either remove reds or make a subset of reds
# Generate a sungraph from the Black vertices https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.subgraph.html
# Specifiec that it can be generated from an iterable list
    black_vertices = set()

    s = g.graph["start"]
    t = g.graph["target"]
    
    for vertex, data in g.nodes(data=True):
        if data.get("color") != "red" or vertex in (s, t):
            black_vertices.add(vertex)
    G_noReds = g.subgraph(black_vertices)

    try:
        size = nx.shortest_path_length(G_noReds, source=s, target=t) # Dijkstra = method="dijkstra", BF = method="bellman-ford"
    except nx.NetworkXNoPath:
        return G_noReds,-1
    # Holds true and it must be possible to gen a shortpath
    return G_noReds,size
    

    