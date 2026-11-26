import statistics
import sys
import networkx as nx
import GraphBuilder as gb
import benchmark

# Selected from a scan of data/: s,t connected, measurable runtime, and (where
# possible) a non-zero answer so that the red-vertex cost actually matters.
FILES = (
    [f"common-1-{n}" for n in (2500, 3500, 4500, 5757)]
    + [f"common-2-{n}" for n in (1000, 2000, 3000, 4000, 5000, 5757)]
    + [f"rusty-1-{n}" for n in (3000, 3500, 4000, 5757)]
    + [f"rusty-2-{n}" for n in (2000, 3000, 4000, 5000, 5757)]
    + [f"gnm-{a}" for a in ("1000-1500-1", "2000-3000-1", "3000-4500-1",
                            "4000-6000-1", "5000-10000-0", "5000-10000-1")]
    + ["grid-25-2", "grid-50-0", "grid-50-2", "smallworld-40-1", "smallworld-50-1",
       "increase-n500-1", "increase-n500-2", "increase-n500-3", "bht"]
)

ALGORITHMS = {
    "Dijkstra": nx.dijkstra_path_length,
    "Bellman-Ford": nx.bellman_ford_path_length,
}
REPEATS = 7


def few_with(algorithm, g):
    """Mirrors problems/few.py (weight 1 on every edge entering a red vertex,
    0 otherwise, then a shortest path) with a pluggable algorithm. Returns the
    number of red vertices on the best s,t-path (s counts), or -1."""
    s, t = g.graph["start"], g.graph["target"]
    nodes = g.nodes
    for u, v in g.edges:
        g.edges[u, v]["weight"] = 1 if nodes[v]["color"] == "red" else 0
    try:
        dist = algorithm(g, source=s, target=t, weight="weight")
    except nx.NetworkXNoPath:
        return -1
    return dist + (1 if nodes[s]["color"] == "red" else 0)


def time_it(fn, *args):
    times = []
    result = None
    for _ in range(REPEATS):
        start = benchmark.GetTime()
        result = fn(*args)
        times.append(benchmark.GetTime() - start)
    return statistics.median(times), min(times), result


def main():
    files = sys.argv[1:] or FILES
    print("| File | n | m | Algorithm | Result | Median (ms) | Min (ms) |")
    print("|---|---|---|---|---|---|---|")
    for name in files:
        G = gb.GraphBuilder.BuildGraph(f"data/{name}.txt")
        results = {}
        for algo_name, algo in ALGORITHMS.items():
            med, best, res = time_it(few_with, algo, G)
            results[algo_name] = res
            print(f"| {name} | {G.number_of_nodes()} | {G.number_of_edges()} | {algo_name} "
                  f"| {res} | {med / 1e6:.3f} | {best / 1e6:.3f} |", flush=True)
        if len(set(results.values())) != 1:
            print(f"WARNING: algorithms disagree on {name}: {results}", file=sys.stderr)


if __name__ == "__main__":
    main()
