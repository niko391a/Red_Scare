import networkx as nx
import GraphBuilder as gb
import GraphDrawer as gd
# import benchmark
from problems.none import none
from problems.few import few
from problems.many import manydp
from problems.alternate import alternate
from problems.some import some
import sys

SHOULD_DRAW = False
FILEPATH = "data/increase-n500-3.txt"

# Format function to adhere to example table
def fmt(value):
    if value is None or value == -1:
        return "-1"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)

def RunNone(G):
    _, size = none(G)
    #print("Length of None: ", size)
    return size

def RunFew(G):
    _, size = few(G)
    #print("Few: ", size)
    return size

def RunMany(G,isdag):
    #print("Many: ", size)
    return manydp(G,isdag)
    
def RunAlternate(G):
    #print("Alternate: ", alternate(G))
    return alternate(G)
    
def RunSome(G, isDAG):
    #print(f"Some: {some(G)}")
    return some(G, isDAG)

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else FILEPATH
    # Parse file to generate graph
    G = gb.GraphBuilder.BuildGraph(path)

    print("n: ", G.number_of_nodes())
    
    A = RunAlternate(G)
    F = RunFew(G)
    N = RunNone(G)
    M = S = "?!" # keeps "NP-hard" if the problem is NP-hard
    
    if G.graph["directed"]:
        if nx.is_directed_acyclic_graph(G): # DAG Directed Acyclic
            M = RunMany(G,True)
            S = RunSome(G, True)
    else: # is undirected
        if nx.is_forest(G.to_undirected()): # undirected Asyclic.
            M = RunMany(G,False)
        S = RunSome(G, False)

    # If M or S is NOT run above they are NP-hard.

    print(f"{G.number_of_nodes():,}", *map(fmt, [A, F, M, N, S]), sep="\t")

    if SHOULD_DRAW and "--no-draw" not in sys.argv:
        gd.DrawGraph(G)

if __name__ == "__main__":
    main()