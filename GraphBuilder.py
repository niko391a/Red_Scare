import os
import networkx as nx

"""
A class for parsing graphs.
Args:
    filepath: path for the file to be parsed.
"""
class GraphBuilder:

    def BuildGraph(filepath):
        G = nx.DiGraph()
        # File name (e.g. "grid-5-0"): used by GraphDrawer for the title and layout choice
        G.graph["name"] = os.path.splitext(os.path.basename(filepath))[0]

        with open(filepath, encoding="utf-8") as f:
            n, m, r = map(int, next(f).split())
            s, t = next(f).split()
            G.graph["start"] = s
            G.graph["target"] = t

            # Building a vertex
            for _ in range(n):
                vertex = next(f).strip().split(" ")
                
                # if it has a star '*' the collection will be larger than 1 
                if len(vertex) > 1:
                    G.add_node(vertex[0], color="red")
                    # No sanity check for now not checking reds count
                    #print("Red " + vertex[0])
                else:
                    G.add_node(vertex[0], color="black")
                    #print("black " + vertex[0])
            
            G.graph["directed"] = False # Tag for directed or undirected
            # Building an edge    
            for _ in range(m):
                a, edge, b = next(f).strip().split(" ")

                if edge == "--": # Undirected
                    G.add_edge(a,b)
                    G.add_edge(b,a)
                    #print("un-directed edge between " + a,b)
                else: # Directed
                    G.graph["directed"] = True
                    G.add_edge(a,b)
                    #print("directed edge between " + a,b)
            # print("-----Sanity Check -----")
            # print(m,n,r,s,t)
            # print(G.graph["start"])
            # print(G.graph["target"])
        return G