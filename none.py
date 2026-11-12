import networkx as nx

class no_reds:
    def No_reds_shortespath(DiGraph g):
# Needs to take the verticies from the redset and remove them from the graphs, verticies. Then run BFS
# If it not possible -1 if it is possible the length of the pass.
    # Idea either remove reds or make a subset of reds

# Generate a sungraph from the Black verticies https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.subgraph.html
# Specifiec that it can be generated from an iterable list
        black_verticies = []
        for verticie, data in G.nodes(data=True):
            if data.get("color") != "Red":
                black_verticies.append(verticie)
        G_noReds = g.subgraph(black_verticies)

        return G_noReds
    