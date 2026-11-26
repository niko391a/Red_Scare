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
  
    # Bound-based fallback depending on resulsts of already calculated values
    if M == "?!":
        n_red_vertices = 0
        for _, color in G.nodes(data="color"):
            if color == "red": n_red_vertices += 1

        if F == -1: # no s, t path at all
            M = -1
        elif S is False: # paths exist but none touch a red vertex
            M = 0
        elif F == n_red_vertices: # even the minimum uses every red vertex so many must also use all
            M = n_red_vertices
        elif S is True and n_red_vertices == 1: # some path hits the single red vertex
            M = 1

    # If M or S is still "?!" then this graph lies outside the classes our algorithms handle and the problem is NP-hard.

    print(f"{G.number_of_nodes():,}", *map(fmt, [A, F, M, N, S]), sep="\t")

    if SHOULD_DRAW and "--no-draw" not in sys.argv:
        gd.DrawGraph(G)

if __name__ == "__main__":
    main()