# Return true if there is a path from s to t that includes at least one red vertex.
# Else return false

# If BFS(G, s, t, []) 

# Based on implementation from https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/
def dfs_rec(visited, current_node, g, target, has_a_red_so_far):

    if current_node == target:
        if has_a_red_so_far: return True
        else: return False

    # Process the node (e.g., print it)
    if g.nodes[current_node]['color'] == "red":
        has_a_red_so_far = True

    visited.add(current_node)

    # Recursive call
    for neighbor in g.neighbors(current_node): 
        if neighbor not in visited:
            if dfs_rec(
                visited,
                neighbor,
                g,
                target,
                has_a_red_so_far
            ): return True

    # Dead end remove
    visited.remove(current_node)
    return False


def some(g):
    start_vertex =  g.graph["start"]
    target_vertex = g.graph["target"]
    visited = set()
    is_some = dfs_rec(visited, start_vertex, g, target_vertex, False)
    return is_some 



# Must check for reds in the path and not the search itself
# This is for cases where reds are a dead end (simple paths only)

# Visited local to the current path
# Push has a red for the current local visited
# So new visited collection for each branching path