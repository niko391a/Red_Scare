import matplotlib.pyplot as pl
import networkx as nx
import GraphBuilder as gb

def main(filepath):
    print("Hello World")

    # Parse file to generate graph
    G = gb.GraphBuilder.BuildGraph(filepath)
    colors = [G.nodes[v]["color"] for v in G.nodes]
    nx.draw(G, with_labels=True, node_color=colors, font_color="lightblue")
    pl.show()

path = "data/wall-n-100.txt"
# path = "data/common-1-20.txt"
main(path)