import networkx as nx
import GraphBuilder as gb
# import benchmark
from problems.none import none
from problems.few import few
from problems.many import many
from problems.alternate import alternate

SHOULD_DRAW = False
FILEPATH = "data/ski-level3-3.txt"

def RunNone(G):
    graph, size = none(G)

    print("Length of None: ", size)
    '''
    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph)
    '''


def RunFew(G):
    graph, size = few(G)
    print("few: amount of red verticies: ", size)

    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph)

def RunMany(G):
    graph, size = many(G)
    print("Many: Most reds: ", size)
    '''
    if SHOULD_DRAW:
            gb.GraphBuilder.DrawGraph(graph)
    '''
def RunAlternate(G):
    print("is alternate: ", alternate(G))
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
            RunAlternate(G)
        else:
            RunNone(G)
            RunFew(G)
            # directed with cycles
            print("Many is Np Hard") # many us NP-Hard of directed with cycles
            RunAlternate(G)
    else: # is undirected
        if nx.is_forest(G): # undirected Asyclic.
            RunNone(G)
            RunFew(G)
            RunMany(G)
            RunAlternate(G)
        else:
            RunNone(G)
            RunFew(G)
            print("Many is Np Hard")  # undirected with cycles: Many is NP-hard
            RunAlternate(G)
        pass

if __name__ == "__main__":
    main()