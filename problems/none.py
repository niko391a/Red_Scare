import networkx as nx
# https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html

def No_reds_shortespath(g):
# Needs to take the verticies from the redset and remove them from the graphs, verticies. Then run BFS
# If it not possible -1 if it is possible the length of the pass.
    # Idea either remove reds or make a subset of reds
# Generate a sungraph from the Black verticies https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.subgraph.html
# Specifiec that it can be generated from an iterable list
    black_verticies = []

    # start_vertex =  g.nodes[g.graph["start"]]['color']
    # target_vertex = g.nodes[g.graph["target"]]['color']
    start_vertex =  g.nodes[g.graph["start"]]
    target_vertex = g.nodes[g.graph["target"]]
    
    # If start or target vertex is red, return -1
    if start_vertex['color'] == 'red' or target_vertex['color'] == 'red':
        return g,-1

    for verticie, data in g.nodes(data=True):
        if data.get("color") != "red":
            black_verticies.append(verticie)
    G_noReds = g.subgraph(black_verticies)

    try:
        size = nx.shortest_path_length(G_noReds, source=g.graph["start"], target=g.graph["target"] method=unweighted)
    except:
        return G_noReds,-1
    # Holds true and it must be possible to gen a shortpath
    return G_noReds,size
    

    