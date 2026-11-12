import networkx as nx
import GraphBuilder as gb
from problems.none import No_reds_shortespath as nr

def main(filepath):
    print("Hello World")

    # Parse file to generate graph
    G = gb.GraphBuilder.BuildGraph(filepath)
    graph, size = nr(G)
    print("size ", size)
    gb.GraphBuilder.DrawGraph(graph)
    

if __name__ == "__main__":
    main("data/ski-level20-2.txt")