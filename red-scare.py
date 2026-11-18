import networkx as nx
import GraphBuilder as gb
import benchmark
from problems.none import none
from problems.few import few
from problems.many import many

SHOULD_DRAW = True
FILEPATH = "data/ski-level3-3.txt"

def RunNone(G):
    # start = benchmark.GetTime()
    # graph, size = nr(G)
    RunNone(G)
    # end = benchmark.GetTime()
    # benchmark.PrintFormattedTime("None", FILEPATH, "BFS", end - start)

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
    RunNone(G)

if __name__ == "__main__":
    main()