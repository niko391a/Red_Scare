import networkx as nx
import GraphBuilder as gb
import GraphDrawer as gd
# import benchmark
from problems.none import none
from problems.few import few
from problems.many import manydp
from problems.alternate import alternate
from problems.some import some

SHOULD_DRAW = False
FILEPATH = "data/increase-n500-3.txt"

def RunNone(G):
    graph, size = none(G)

    print("Length of None: ", size)
    '''
    if SHOULD_DRAW:
            gd.DrawGraph(graph)
    '''


def RunFew(G):
    graph, size = few(G)
    print("Few: ", size)

    if SHOULD_DRAW:
            gd.DrawGraph(graph)

def RunMany(G,isdag):
    size = manydp(G,isdag)
    print("Many: ", size)
    '''
    if SHOULD_DRAW:
            gd.DrawGraph(graph)
    '''
def RunAlternate(G):
    print("Alternate: ", alternate(G))
    '''
    if SHOULD_DRAW:
            gd.DrawGraph(graph)
    '''
def RunSome(G):
    print(f"Some: {some(G)}")
    '''
    if SHOULD_DRAW:
        gd.DrawGraph(G)
    '''

def main():
    # Parse file to generate graph
    G = gb.GraphBuilder.BuildGraph(FILEPATH)
    print("n: ", G.number_of_nodes())
    RunAlternate(G)
    RunFew(G)
    if G.is_directed():
        if nx.is_directed_acyclic_graph(G): # DAG Directed Acyclic
            RunMany(G,True)
            RunSome(G)
        else:
            # directed with cycles
            print("Many is Np Hard") # many us NP-Hard of directed with cycles
            print("Some is Np Hard")
    else: # is undirected
        if nx.is_forest(G): # undirected Asyclic.
            RunMany(G,False)
            RunSome(G)
        else:
            print("Many is Np Hard")  # undirected with cycles: Many is NP-hard
            print("Some is Np Hard")
        pass
    RunNone(G)

if __name__ == "__main__":
    main()