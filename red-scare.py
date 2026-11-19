import networkx as nx
import GraphBuilder as gb
# import benchmark
from problems.none import none
from problems.few import few
from problems.many import many

SHOULD_DRAW = True
FILEPATH = "data/ski-level3-3.txt"

def RunNone(G):
    graph, size = none(G)

    print("size None ", size)
    '''
    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph)
    '''


def RunFew(G):
    graph, size = few(G)
    print("size few", size)
    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph)

def RunMany(G):
    graph, size = many(G)
    print("size many ", size)
    '''
    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph)
    '''
            
def main():
    # Parse file to generate graph
    G = gb.GraphBuilder.BuildGraph(FILEPATH)
    if G.is_directed():
        if nx.is_directed_acyclic_graph(G): # DAG Directed Acyclic
            print("Is DAG")
            RunNone(G)
            RunFew(G)
            RunMany(G)
        else:
            RunNone(G)
            RunFew(G)
            # directed with cycles
            print("Many is Np Hard") # many us NP-Hard of directed with cycles
    else: # is undirected
        if nx.is_forest(G): # undirected Asyclic.
            RunNone(G)
            RunFew(G)
            RunMany(G)
        else:
            RunNone(G)
            RunFew(G)
            print("Many is Np Hard")  # undirected with cycles: Many is NP-hard
        pass

if __name__ == "__main__":
    main()