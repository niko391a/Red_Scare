# Return the maximum number of of red vertices on any path from s to t
# Else return -1 if there is no path from s to t
import networkx as nx
'''
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

'''



def manydp(G,isdag):
    '''
    First get the red set of all red verticies

    Then check weheter a path exist from s to t at all

    Then:
        If it is directed an acyclic then we
        create we put a weight of 1 on all edges going to a red vertici
        This will pick the most expensive route.

        Then formm a sub graph made of all s,t paths
        And takes the most expensive if start and finsih is black, it dosent add to the amount, but we check wheter s is in red and add that incase it is since t is already acounted for by the 
        longestpathlength algorithm
        This is O(V+E)


    Else:
        We gen the path since there is only one path the O(V+E*P) p effectively becomes 1 resulting in O(V+E)
        So we loop through all the reds and count them in the for loop

    '''
    g = G.copy()
    red_vertices = set()
    for vertex, data in g.nodes(data=True):
            if data.get("color") == "red":
                red_vertices.add(vertex)

    # So for this to work we need to define the start and target
    s, t = g.graph["start"], g.graph["target"]
    # Then need to remove all the noise so the once that arent reachable just incase, it might be disjointed and all the reds can be connected from s to t
    # if no exist it should be -1
    if not nx.has_path(g, s, t):
        return -1

    if isdag: 

        for (u,v) in g.edges:
            if v in red_vertices:
                g.edges[u,v]['weight'] = 1
            else:
                g.edges[u,v]['weight'] = 0




        reachable_from_s = nx.descendants(g, s) | {s}
        can_reach_t = nx.ancestors(g, t) | {t}
   
        sub = g.subgraph(reachable_from_s & can_reach_t).copy() # Sub graph containing all that is reachable from s and t Meaning it Contains P all paths of s,t

        
        size = nx.dag_longest_path_length(sub, weight="weight") # Libabry implementation of longesth path based on weight o(v+e)
        return size + (1 if s in red_vertices else 0) # adde

        
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

