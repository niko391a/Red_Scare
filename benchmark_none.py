import contextlib
import io
import statistics
import sys
import networkx as nx
import GraphBuilder as gb
import benchmark
from problems.none import No_reds_shortespath as nr

FILES = (
    [f"wall-n-{n}" for n in (1, 10, 100, 1000, 10000)]
    + [f"rusty-1-{n}" for n in (2000, 3000, 4000, 5000, 5757)]
    + [f"rusty-2-{n}" for n in (2000, 3000, 4000, 5000, 5757)]
    + [f"gnm-{a}" for a in ("1000-2000-0", "2000-4000-0", "3000-6000-0", "4000-8000-0")]
)
FILES = [f for f in FILES if f != "rusty-1-2000"]  # no red-free path

ALGORITHMS = {
    "BFS": nx.shortest_path_length,
    "Dijkstra": nx.dijkstra_path_length,
    "Bellman-Ford": nx.bellman_ford_path_length,
}
REPEATS = 7


def no_reds_with(algorithm, g):
    """Same edge-case handling as No_reds_shortespath, with a pluggable algorithm."""
    s, t = g.graph["start"], g.graph["target"]
    if g.nodes[s]["color"] == "red" or g.nodes[t]["color"] == "red":
        return -1
    sub = g.subgraph(n for n, d in g.nodes(data=True) if d.get("color") != "red")
    try:
        return algorithm(sub, source=s, target=t)
    except nx.NetworkXNoPath:
        return -1


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
        # Sanity check against the real implementation (prints suppressed by caller's stdout)
        results = {}
        for algo_name, algo in ALGORITHMS.items():
            med, best, res = time_it(no_reds_with, algo, G)
            results[algo_name] = res
            print(f"| {name} | {G.number_of_nodes()} | {G.number_of_edges()} | {algo_name} "
                  f"| {res} | {med / 1e6:.3f} | {best / 1e6:.3f} |", flush=True)
        if len(set(results.values())) != 1:
            print(f"WARNING: algorithms disagree on {name}: {results}", file=sys.stderr)
        with contextlib.redirect_stdout(io.StringIO()):  # silence nr()'s prints
            nr_result = nr(G)[1]
        if nr_result != results["BFS"]:
            print(f"WARNING: nr() disagrees with BFS on {name}", file=sys.stderr)


if __name__ == "__main__":
    main()
