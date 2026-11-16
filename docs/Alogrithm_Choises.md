# Choice of Algorithm


# None
---
When first looking at the charecteristics of what none needed, we quickly settle on, That we would need a shortest path algorithm, since it asked for the shortest path.
We have explored several, the Dijkstra,BFS and Bellman ford.

To figure out how we got the shortest path without any reds if possible an Idea came to mind, What if we removed all the red nodes/verticies from the graph then ran a shortes path alogrithm. This is what we ended up implementing we generated a subgrap meaning copying all the edges and notes, here we looked at the atributed if it was red or black, and only inluded the black notes and their edges got copied when generating the subgraph and edges to reds was removed.

From this we could run the BFS, on the subgraph, with a condition check to see if the start or end was red or not finishing -1 else the length of the shortest path was returned