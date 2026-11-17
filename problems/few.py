# Return the minimum number of red vertices on any path from s to t
# Else return -1 if no path exists
# upgrade to a weighted graph, where the edge between a black to red or red to red is set at max, this is like the ferry to bornholm in map of denmark
# Meaning that if no other path exist from source to target, then we are forced to touch the red increasing the weight
# And it will go for the lowest weighted to gen a shortest path Using bellman ford or dijkstra, since no negative dijkstra is probably better
# black→red: 100
# red→red: 100
# red→black: 0
# black→black: 0
# These are the cases
# At the same time, count the amount of reds you meet on the way
import networkx as nx

def few(g):
    red_verticies = []
    for vertice, data in g.nodes(data=True):
            if data.get("color") == "red":
                red_verticies.append(vertice)
    '''
            -------
        edges : OutEdgeView
            A view of edge attributes, usually it iterates over (u, v)
            or (u, v, d) tuples of edges, but can also be used for
            attribute lookup as `edges[u, v]['foo']`.

        See Also
        --------
    '''
    for (u,v) in g.edges:
        if v in red_verticies:
            g.edges[u,v]['weight'] = 1000
        else:
            g.edges[u,v]['weight'] = 0

    try:
        path = nx.shortest_path(g, source=g.graph["start"], target=g.graph["target"],weight="weight", method="dijkstra") # targers unweighted that is BFS = "unweighted"
    except:
        print("fucked up 2")
        return g,-1
    # path is a list of verticies / nodes
    redcount = 0
    for v in path:
        if v in red_verticies:
              redcount += 1
    
    return g.redcount