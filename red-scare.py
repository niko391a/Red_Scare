import networkx as nx
import GraphBuilder as gb

def main(filepath):
    print("Hello World")

    # Parse file to generate graph
    G = gb.GraphBuilder.BuildGraph(filepath)
    gb.GraphBuilder.DrawGraph(G)

if __name__ == "__main__":
    main("data/wall-n-1.txt")