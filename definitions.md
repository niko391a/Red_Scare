# Definitions

## Graph
- $G$: The graph (can be directed or undirected).
- $V(G)$: The set of vertices in graph $G$.
- $E(G)$: The set of edges in graph $G$.
- $n=|V(G)|$: The number of vertices in graph $G$.
- $m=|E(G)|$: The number of edges in graph $G$.
- $s \in V(G)$: The start vertex in graph $G$.
- $t \in V(G)$: The end vertex in graph $G$.
- $R \in V(G)$: The subset of red vertices in graph $G$  (can include $s$ or $t$).
- $r=|R|$: The number of red vertices in graph $G$.

## Path
$s,t-path$: A sequence of distinct vertices $v_i,v_{i+1}$ where:
- $v_1=s$
- $v_l=t$
- $v_i,v_{i+1} \in E(G)$

For each $i \in \{1,...,l-1\}$.

The length of such a path is $l-1$ (the number of edges).