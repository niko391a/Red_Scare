import networkx as nx
import GraphBuilder as gb
# import benchmark
from problems.alternate import alternate
from problems.none import none
from problems.few import few
from problems.many import many

SHOULD_DRAW = True
FILEPATH = "data/grid-5-0.txt"

def RunAlternate(G):
    hasPath = alternate(G)
    print(f"Is there an alternating path: {hasPath}")
    if SHOULD_DRAW:
        gb.GraphBuilder.DrawGraph(G)

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
    RunAlternate(G)

if __name__ == "__main__":
    main()