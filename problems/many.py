# Return the maximum number of of red vertices on any path from s to t
# Else return -1 if there is no path from s to t
import networkx as nx

def many(g): # old bruteforce 
    red_vertices = set()
    for vertex, data in g.nodes(data=True):
            if data.get("color") == "red":
                red_vertices.add(vertex)
    maxi = -1
    try:
        for path in nx.all_simple_paths(g, source=g.graph["start"], target=g.graph["target"]): # Get all simple paths
            redcount = 0
            for v in path:
                    if v in red_vertices:
                          redcount += 1
            maxi=max(redcount,maxi)      
    except:
        print("fucked up 2")
        return g,-1
    # path is a list of vertices / nodes
    return g,maxi





def manydp(g,isdag):

    red_vertices = set()
    for vertex, data in g.nodes(data=True):
            if data.get("color") == "red":
                red_vertices.add(vertex)

    if isdag: 

        for (u,v) in g.edges:
            if v in red_vertices:
                g.edges[u,v]['weight'] = 1
            else:
                g.edges[u,v]['weight'] = 0


        # So for this to work we need to define the start and target
        s, t = g.graph["start"], g.graph["target"]
        # Then need to remove all the noise so the once that arent reachable just incase, it might be disjointed and all the reds can be connected from s to t
        # if no exist it should be -1
        if not nx.has_path(g, s, t):
            return -1
        else:
            reachable_from_s = nx.descendants(g, s) | {s}
            can_reach_t = nx.ancestors(g, t) | {t}
   
            sub = g.subgraph(reachable_from_s & can_reach_t).copy() # Sub graph containing all that is reachable from s and t Meaning it Contains P all paths of s,t

        
            size = nx.dag_longest_path_length(sub, weight="weight") # Libabry implementation of longesth path based on weight o(v+e)
            return size

        
    else:
        maxi = -1
        
        for path in nx.all_simple_paths(g, source=g.graph["start"], target=g.graph["target"]): # Get all simple paths
            redcount = 0
            for v in path:
                    if v in red_vertices:
                          redcount += 1
            maxi=max(redcount,maxi)      
            # path is a list of vertices / nodes
        return maxi



    
def manydp(g,isdag):

    red_vertices = set()
    for vertex, data in g.nodes(data=True):
            if data.get("color") == "red":
                red_vertices.add(vertex)

    if isdag: 

        for (u,v) in g.edges:
            if v in red_vertices:
                g.edges[u,v]['weight'] = 1
            else:
                g.edges[u,v]['weight'] = 0


        # So for this to work we need to define the start and target
        s, t = g.graph["start"], g.graph["target"]
        # Then need to remove all the noise so the once that arent reachable just incase, it might be disjointed and all the reds can be connected from s to t
        # if no exist it should be -1
        if not nx.has_path(g, s, t):
            return -1
        else:
            reachable_from_s = nx.descendants(g, s) | {s}
            can_reach_t = nx.ancestors(g, t) | {t}
   
            sub = g.subgraph(reachable_from_s & can_reach_t).copy() # Sub graph containing all that is reachable from s and t Meaning it Contains P all paths of s,t

        
            size = nx.dag_longest_path_length(sub, weight="weight") # Libabry implementation of longesth path based on weight o(v+e)
            return size + (1 if s in red_vertices else 0)

        
    else:
        maxi = -1
        
        for path in nx.all_simple_paths(g, source=g.graph["start"], target=g.graph["target"]): # Get all simple paths
            redcount = 0
            for v in path:
                    if v in red_vertices:
                          redcount += 1
            maxi=max(redcount,maxi)      
            # path is a list of vertices / nodes
        return maxi