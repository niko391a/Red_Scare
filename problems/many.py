# Return the maximum number of of red vertices on any path from s to t
# Else return -1 if there is no path from s to t
import networkx as nx

def many(g):
    red_vertices = set()
    for vertex, data in g.nodes(data=True):
            if data.get("color") == "red":
                red_vertices.add(vertex)
    maxi = 0
    try:
        for path in nx.all_simple_paths(g, source=g.graph["start"], target=g.graph["target"]): # Get all simple paths
            redcount = 0
            for v in path:
                    if v in red_vertices:
                          redcount =+ 1
                    maxi=max(redcount,maxi)      
    except:
        print("fucked up 2")
        return g,-1
    # path is a list of vertices / nodes
    return g,maxi

#Not working