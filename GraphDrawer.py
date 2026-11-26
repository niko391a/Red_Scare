"""
Utility methods defined entirely by Claude.
So all credit to it.

Drawing of Red Scare graphs built by GraphBuilder.BuildGraph.

Usage:
    import GraphDrawer as gd
    gd.DrawGraph(G)                          # open a window
    gd.DrawGraph(G, path=[...])              # highlight a path (e.g. a solution)
    gd.DrawGraph(G, save_to="grid-5-0.png")  # save instead of showing
"""
import math
import re

import networkx as nx
import matplotlib.pyplot as pl
from matplotlib.lines import Line2D

# Palette: high contrast on a white background
RED = "#d62728"        # vertices in R
PLAIN = "#ffffff"      # vertices not in R
OUTLINE = "#333333"    # default node outline
START = "#2ca02c"      # ring around s
TARGET = "#1f77b4"     # ring around t
PATH = "#ff7f0e"       # highlighted path
EDGE = "#888888"

COORD_NAME = re.compile(r"^\d+_\d+$")  # grid / smallworld vertex names, e.g. "3_4"


def DrawGraph(G, path=None, max_nodes=300, radius=2, save_to=None):
    """
    Draw G with a layout suited to its graph family.

    path:      optional list of vertices to highlight (falls back to G.graph["path"]).
    max_nodes: larger graphs are cut down to the neighbourhood of s, t and the path.
    radius:    hop distance used for that neighbourhood.
    save_to:   file name to save the figure to instead of opening a window.
    """
    s, t = G.graph["start"], G.graph["target"]
    name = G.graph.get("name", "")
    path = list(path if path is not None else G.graph.get("path") or [])

    H, note = _restrict(G, s, t, path, max_nodes, radius)
    pos, kind = _layout(G, H, name, t)
    n = len(H)

    # Scale nodes/labels by how many vertices are on screen
    node_size = 500 if n <= 30 else 250 if n <= 100 else 60 if n <= 300 else 15
    max_label = max((len(str(v)) for v in H), default=0)
    labels_inside = max_label <= 3 and node_size >= 250
    show_labels = n <= 120

    if kind == "line":
        fig, ax = pl.subplots(figsize=(min(30, max(10, n * 0.5)), 4))
    elif kind in ("coords", "ski"):
        fig, ax = pl.subplots(figsize=(10, 10))
    else:
        fig, ax = pl.subplots(figsize=(12, 9))

    # ---- edges ----
    path_edges = set(zip(path, path[1:]))
    on_path = lambda u, v: (u, v) in path_edges or (v, u) in path_edges

    # BuildGraph stores an undirected edge as u->v plus v->u. Draw such pairs once, without arrows.
    undirected, directed = [], []
    for u, v in H.edges():
        if on_path(u, v):
            continue
        if H.has_edge(v, u):
            if str(u) < str(v):  # keep only one of the two copies
                undirected.append((u, v))
        else:
            directed.append((u, v))

    m_shown = len(undirected) + len(directed)
    alpha = 0.7 if m_shown < 300 else 0.35 if m_shown < 2000 else 0.15
    # Increase graphs: every arc points right along one line, so bend them into arcs
    conn = "arc3,rad=-0.35" if kind == "line" else "arc3"

    if undirected:
        nx.draw_networkx_edges(H, pos, edgelist=undirected, ax=ax, arrows=False,
                               edge_color=EDGE, alpha=alpha, width=1.2)
    if directed:
        nx.draw_networkx_edges(H, pos, edgelist=directed, ax=ax, arrows=True,
                               arrowstyle="-|>", arrowsize=12 if n <= 100 else 6,
                               node_size=node_size,  # stops arrowheads at the node border
                               connectionstyle=conn, edge_color=EDGE, alpha=alpha, width=1.2)
    shown_path = [e for e in zip(path, path[1:]) if e[0] in H and e[1] in H]
    if shown_path:
        # Path drawn with arrows in travel direction, on top of the other edges
        nx.draw_networkx_edges(H, pos, edgelist=shown_path, ax=ax, arrows=True,
                               arrowstyle="-|>", arrowsize=16, node_size=node_size,
                               connectionstyle=conn, edge_color=PATH, width=3.5)

    # ---- nodes ----
    nodes = list(H)
    fill = [RED if H.nodes[v]["color"] == "red" else PLAIN for v in nodes]
    ring = [START if v == s else TARGET if v == t else OUTLINE for v in nodes]
    ring_w = [3.5 if v in (s, t) else 1.0 for v in nodes]
    nx.draw_networkx_nodes(H, pos, nodelist=nodes, ax=ax, node_size=node_size,
                           node_color=fill, edgecolors=ring, linewidths=ring_w)

    # s and t are always labelled, even on big graphs
    label_nodes = nodes if show_labels else [v for v in (s, t) if v in H]
    if labels_inside:
        # White text on red nodes, black on white ones
        for want_red, colour in ((True, "white"), (False, "black")):
            group = {v: v for v in label_nodes if (H.nodes[v]["color"] == "red") == want_red}
            nx.draw_networkx_labels(H, pos, labels=group, ax=ax,
                                    font_size=10 if n <= 30 else 7, font_color=colour)
    else:
        # Long names (words) do not fit in a node: put them just below it on a white box
        xs = [p[0] for p in pos.values()]
        ys = [p[1] for p in pos.values()]
        span = max(max(xs) - min(xs), max(ys) - min(ys), 1e-9)
        label_pos = {v: (pos[v][0], pos[v][1] - 0.03 * span) for v in label_nodes}
        nx.draw_networkx_labels(H, label_pos, labels={v: v for v in label_nodes}, ax=ax,
                                font_size=9 if n <= 60 else 7, verticalalignment="top",
                                bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=0.5))

    # ---- legend & title (stats are for the whole graph, not the cut-down view) ----
    r = sum(1 for v in G if G.nodes[v]["color"] == "red")
    two_way = sum(1 for u, v in G.edges() if G.has_edge(v, u))
    m = two_way // 2 + (G.number_of_edges() - two_way)
    direction = ("undirected" if two_way == G.number_of_edges()
                 else "directed" if two_way == 0 else "mixed")

    handles = [
        Line2D([], [], marker="o", ls="", ms=10, mfc=RED, mec=OUTLINE, label=f"red (r = {r})"),
        Line2D([], [], marker="o", ls="", ms=10, mfc=PLAIN, mec=OUTLINE, label="not red"),
        Line2D([], [], marker="o", ls="", ms=10, mfc="none", mec=START, mew=3, label=f"start s = {s}"),
        Line2D([], [], marker="o", ls="", ms=10, mfc="none", mec=TARGET, mew=3, label=f"target t = {t}"),
    ]
    if path_edges:
        handles.append(Line2D([], [], color=PATH, lw=3.5, label=f"path ({len(path) - 1} edges)"))
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False)

    title = f"{name}   n={len(G)}  m={m}  r={r}   [{direction}]"
    if note:
        title += f"\n{note}"
    ax.set_title(title)
    ax.axis("off")
    ax.margins(0.08)
    if kind == "line":
        # Arcs are bent in screen space (height ~0.18 * on-screen length), not data space,
        # so the y-limits only decide where the row sits: near the bottom, arcs above it
        ax.set_ylim(-1, 3)
    else:
        ax.set_aspect("equal")  # keep grid squares square and cycles round
    fig.tight_layout()

    if save_to:
        fig.savefig(save_to, dpi=150, bbox_inches="tight")
        pl.close(fig)
    else:
        pl.show()


# ---------------------------------------------------------------- helpers

def _restrict(G, s, t, path, max_nodes, radius):
    """Big graphs are an unreadable hairball: keep only vertices near s, t and the path."""
    if len(G) <= max_nodes:
        return G, ""
    U = G.to_undirected(as_view=True)  # "near" ignores edge direction
    seeds = {s, t, *path}
    # Shrink the radius until the neighbourhood fits (dense graphs blow up quickly)
    for rad in range(radius, -1, -1):
        keep = set(seeds)
        for v in seeds:
            if v in U:
                keep.update(nx.single_source_shortest_path_length(U, v, cutoff=rad))
        if len(keep) <= max_nodes:
            break
    what = "s, t and the path" if path else "s and t"
    return G.subgraph(keep), f"showing {len(keep)} of {len(G)} vertices: within {rad} steps of {what}"


def _layout(G, H, name, t):
    """Pick positions matching the structures described in the assignment's graph gallery."""
    nodes = list(H)

    # Grid and smallworld graphs: vertex names are coordinates "x_y"
    if nodes and all(COORD_NAME.match(str(v)) for v in nodes):
        return {v: tuple(map(int, v.split("_"))) for v in nodes}, "coords"

    # Ski: ids are numbered row by row in a triangle, t is a sink below the last row
    if name.startswith("ski"):
        try:
            return _ski_layout(H, t), "ski"
        except ValueError:
            pass  # non-numeric names: use a generic layout instead

    # Increase: the sequence order is the file order, so put the vertices on a line in that order
    if name.startswith("increase"):
        order = [v for v in G if v in H]  # DiGraph keeps insertion (= file) order
        return {v: (i, 0) for i, v in enumerate(order)}, "line"

    # Any other DAG: top-down layers
    if nx.is_directed_acyclic_graph(H) and H.number_of_edges() > 0:
        pos = {}
        for depth, layer in enumerate(nx.topological_generations(H)):
            layer = sorted(layer, key=str)
            for j, v in enumerate(layer):
                pos[v] = (j - (len(layer) - 1) / 2, -depth)
        return pos, "dag"

    return _force_layout(H), "force"


def _force_layout(H):
    """
    Force-directed layout, one connected component at a time.
    Laying out a disconnected graph in one go pushes the pieces into far corners and squashes
    each piece, so instead each component gets its own layout and they are packed in rows.
    """
    U = H.to_undirected(as_view=True)
    comps = sorted(nx.connected_components(U), key=len, reverse=True)
    row_width = max(2 * math.sqrt(len(H)), math.sqrt(len(comps[0]))) if comps else 1
    pos, x, y, row_h = {}, 0.0, 0.0, 0.0
    for comp in comps:
        C = U.subgraph(comp)
        if len(C) == 1:
            p = {v: (0.0, 0.0) for v in C}
        elif len(C) <= 300:
            p = nx.kamada_kawai_layout(C)  # cleaner for small graphs, but O(n^2)
        else:
            # fixed seed = same picture every run; larger k = more spread out
            p = nx.spring_layout(C, k=1.5 / math.sqrt(len(C)), iterations=100, seed=42)

        # Normalise to a box whose side grows with sqrt(size), so big components get more room
        size = math.sqrt(len(C))
        xs, ys = [q[0] for q in p.values()], [q[1] for q in p.values()]
        span = max(max(xs) - min(xs), max(ys) - min(ys)) or 1.0
        if x > 0 and x + size > row_width:  # row full: start a new one below
            x, y, row_h = 0.0, y - row_h - 1.0, 0.0
        for v, (px, py) in p.items():
            pos[v] = (x + (px - min(xs)) / span * size, y - (max(ys) - py) / span * size)
        x += size + 1.0
        row_h = max(row_h, size)
    return pos


def _ski_layout(H, t):
    """Row k of the mountain holds ids k(k+1)/2 .. k(k+1)/2 + k (see Figure 9 in the PDF)."""
    pos = {}
    for v in H:
        if v == t:
            continue
        i = int(v)                              # ValueError for non-numeric names
        k = (math.isqrt(8 * i + 1) - 1) // 2    # row: largest k with k(k+1)/2 <= i
        p = i - k * (k + 1) // 2                # position within the row
        pos[v] = (p - k / 2, -k)                # centre each row under the start
    bottom = min((y for _, y in pos.values()), default=0)
    pos[t] = (0, bottom - 1.5)
    return pos
