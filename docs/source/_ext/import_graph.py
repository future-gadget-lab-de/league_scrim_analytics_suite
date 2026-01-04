from __future__ import annotations

from pathlib import Path
from typing import Set, Tuple
import os
import networkx as nx


def _collapse(name: str, root: str, internal_depth: int) -> str:
    """
    Collapse modules to keep graphs readable.
    - internal modules: keep root + (internal_depth-1) segments
    - external modules: keep only the top-level package
    """
    parts = name.split(".")
    if name == root or name.startswith(root + "."):
        return ".".join(parts[:internal_depth])
    return parts[0]  # external top-level package (e.g. "requests", "sqlalchemy")


def _write_dot(path: Path, edges: Set[Tuple[str, str]]) -> None:
    lines = [
        "digraph imports {",
        "  rankdir=LR;",
        "  node [shape=box];",
    ]
    for a, b in sorted(edges):
        lines.append(f'  "{a}" -> "{b}";')
    lines.append("}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _adjacent_nodes(G: nx.DiGraph, node: str, level: int, reverse: bool = False) -> set[str]:
    if node not in G:
        return set()  # oder raise, je nachdem was du willst

    visited = {node}
    frontier = {node}

    for _ in range(level):
        if not frontier:
            break

        nxt = set()
        if reverse:
            for u in frontier:
                nxt.update(G.predecessors(u))  # wer importiert u?
        else:
            for u in frontier:
                nxt.update(G.successors(u))    # wen importiert u?

        nxt -= visited
        visited |= nxt
        frontier = nxt

    return visited


def _subgraph(G: nx.DiGraph, n: int, node: str, mode: str = "neighbor") -> nx.DiGraph:
    
    nodes_adj = _adjacent_nodes(G, node, n)
    nodes_adj_reversed = _adjacent_nodes(G, node, n, reverse=True)

    match mode:
        case "neighbor":
            neighbor_nodes = nodes_adj.union(nodes_adj_reversed)
            return G.subgraph(list(neighbor_nodes))
        case "neighbor_reduced":
            return nx.compose(G.subgraph(list(nodes_adj)),G.subgraph(list(nodes_adj_reversed)))
        case "import":
            return G.subgraph(list(nodes_adj))
        case "export":
            return G.subgraph(list(nodes_adj_reversed))



def generate_import_graph(app) -> None:
    import grimp  # local import

    MODES = ["export","import","neighbor", "neighbor_reduced"]
    LEVELS = [1,2,3,4,5]

    root = app.config.depgraph_root_package
    if not root:
        # Nothing to do if not configured
        return

    for ext in [True,False]:

        include_externals = ext
    
        internal_depth = int(app.config.depgraph_internal_depth)

        graph = grimp.build_graph(root, include_external_packages=include_externals)
        imports = graph.find_matching_direct_imports("** -> **")
        #print(imports)

        G_imp = nx.DiGraph()

        for imp in imports:
            #if imp["importer"] == root:# or imp["importer"] in visited_nodes:
                a = _collapse(imp["importer"], root, internal_depth)
                b = _collapse(imp["imported"], root, internal_depth)
                if a != b:
                    G_imp.add_edges_from([(a,b)])

        all_packages: list[str] = sorted(list(G_imp.nodes))

        for package in all_packages:
            for mode in MODES:
                for level in LEVELS:
                    
                    sub = _subgraph(G_imp, level, package, mode)

                    out_dir = Path(app.srcdir) / "_generated"
                    out_dir.mkdir(parents=True, exist_ok=True)
                    name_list = package.split(".")
                    name_list += [str(ext), mode, str(level), ".dot"]
                    filename = "_".join(name_list)
                    _write_dot(out_dir / filename , set(sub.edges))


def setup(app):
    app.add_config_value("depgraph_root_package", None, "env")
    app.add_config_value("depgraph_include_external_packages", True, "env")
    app.add_config_value("depgraph_internal_depth", 2, "env")
    app.add_config_value("depgraph_hierarchie_size", None, "env")

    app.connect("builder-inited", generate_import_graph)

    # Optional, but recommended:
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
