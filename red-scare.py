import networkx as nx
import GraphBuilder as gb
import benchmark
from problems.none import No_reds_shortespath as nr
from problems.few import few
from problems.many import many

SHOULD_DRAW = False
FILEPATH = "data/grid-50-1.txt"

def RunNone(G):
    start = benchmark.GetTime()
    graph, size = nr(G)
    end = benchmark.GetTime()
    print("size ", size)
    benchmark.PrintFormattedTime("None", FILEPATH, "BFS", end - start)

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
    RunNone(G)

if __name__ == "__main__":
    main()