import networkx as nx
import GraphBuilder as gb
import benchmark
from problems.none import none
from problems.few import few
from problems.many import many

SHOULD_DRAW = False
FILEPATH = "data/ski-level3-3.txt"

def RunNone(G):
    graph, size = none(G)
    print("size ", size)
    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph)


def RunFew(G):
    graph, size = few(G)
    print("size ", size)
    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph)

def RunMany(G):
    graph_many, size_many = many(G)
    print("size ", size_many)
    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph_many)
            
def main():
    # Parse file to generate graph
    G = gb.GraphBuilder.BuildGraph(FILEPATH)
    if G.is_directed():
        if nx.is_directed_acyclic_graph(G): # DAG Directed Acyclic
            RunNone(G)
            RunFew(G)
        else:
            RunNone(G)
            RunFew(G)
            # directed with cycles
            print("?!") # many us NP-Hard of directed with cycles
    else: # is undirected
        if nx.is_forest(G): # undirected Asyclic.
            RunNone(G)
            RunFew(G)
        else:
            RunNone(G)
            RunFew(G)
            print("?!")  # undirected with cycles: Many is NP-hard
        pass

if __name__ == "__main__":
    main()