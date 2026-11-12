from collections import deque

# BFS from previous exercise in the code

# PATH-FINDING
def BFS(G, s, t, parent):
    visited = [False] * len(G) # To keep track of the visited nodes in the graph
    
    # Make the queue, add s
    q = deque()
    q.append(s)
    
    # Add s to the list of visited nodes, s has no parent
    visited[s] = True
    parent[s] = -1

    while q:
        u = q.popleft() # Get first element
        for v in range(1, len(G)): # Look through graph to see if there is a connection to u
            if not visited[v] and G[u][v] > 0: # If v is not visited and there is capacity left
                visited[v] = True # Mark v as visited
                parent[v] = u # Set u as v's parent

                if v == t: #If v is equal to the sink, then we have a complete path
                    return True
                q.append(v)

    return False # the queue is empty and the function is still going, then no path has been found
