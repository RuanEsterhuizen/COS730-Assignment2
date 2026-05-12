import os
import ast
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class ClassDependencyAnalyzer(ast.NodeVisitor):
    def __init__(self, module_classes):
        self.module_classes = module_classes
        self.current_class = None
        self.edges = set()

    def visit_ClassDef(self, node):
        previous_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = previous_class

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            class_name = node.func.id
            if (
                self.current_class is not None
                and class_name in self.module_classes
                and class_name != self.current_class  # ✅ filter self-loops
            ):
                self.edges.add((self.current_class, class_name))
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if isinstance(node.annotation, ast.Name):
            class_name = node.annotation.id
            if (
                self.current_class is not None
                and class_name in self.module_classes
                and class_name != self.current_class  # ✅ filter self-loops
            ):
                self.edges.add((self.current_class, class_name))
        self.generic_visit(node)


def collect_classes_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}


def build_class_graph(project_path):
    all_classes = set()

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                try:
                    all_classes.update(collect_classes_from_file(os.path.join(root, file)))
                except Exception:
                    pass

    edges = set()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                    analyzer = ClassDependencyAnalyzer(all_classes)
                    analyzer.visit(tree)
                    edges.update(analyzer.edges)
                except Exception:
                    pass

    edges = {(a, b) for a, b in edges if a is not None and b is not None}
    return all_classes, edges


def classify_nodes(graph):
    """Classify nodes by their role in the dependency graph."""
    isolated = [n for n in graph.nodes if graph.in_degree(n) == 0 and graph.out_degree(n) == 0]
    high_in = sorted(graph.nodes, key=lambda n: graph.in_degree(n), reverse=True)
    high_out = sorted(graph.nodes, key=lambda n: graph.out_degree(n), reverse=True)
    cycles = list(nx.simple_cycles(graph))
    return isolated, high_in, high_out, cycles


def draw_graph(classes, edges):
    graph = nx.DiGraph()
    graph.add_nodes_from(classes)
    graph.add_edges_from(edges)

    isolated, high_in, high_out, cycles = classify_nodes(graph)
    cycle_nodes = {n for cycle in cycles for n in cycle}

    # Colour nodes by role
    node_colors = []
    for node in graph.nodes:
        if node in cycle_nodes:
            node_colors.append("#f28b82")   # red — in a cycle
        elif graph.in_degree(node) == 0 and graph.out_degree(node) == 0:
            node_colors.append("#a8d8a8")   # green — isolated/leaf
        elif graph.in_degree(node) >= 3:
            node_colors.append("#aecbfa")   # blue — heavily depended-upon (shared core)
        elif graph.out_degree(node) >= 3:
            node_colors.append("#fdd663")   # yellow — depends on many others (high coupling)
        else:
            node_colors.append("#e0e0e0")   # gray — normal

    pos = nx.spring_layout(graph, k=2.0, seed=42)

    fig, ax = plt.subplots(figsize=(14, 10))

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=2500, node_color=node_colors, ax=ax)

    # ✅ Fix: use FancyArrowPatch-compatible draw_networkx with connectionstyle
    nx.draw_networkx_edges(
        graph, pos,
        ax=ax,
        arrows=True,    
        arrowsize=20,
        width=1.5,
        edge_color="#777777",
        connectionstyle="arc3,rad=0.15",    # curved edges so bidirectional are distinct
        min_source_margin=25,               # ✅ gap so arrow starts outside the node
        min_target_margin=25,               # ✅ gap so arrowhead lands outside the node
    )

    nx.draw_networkx_labels(graph, pos, font_size=8, ax=ax)

    # Print analysis to console
    print(f"\n{'='*40}")
    print(f"Classes: {len(classes)}  |  Dependencies: {len(edges)}")
    print(f"Cycles detected: {len(cycles)}")
    for c in cycles:
        print(f"  ⚠ {' → '.join(c)} → {c[0]}")
    print(f"Isolated classes (no deps): {isolated}")
    top_depended = high_in[:3]
    print(f"Most depended-upon: {[f'{n} (in={graph.in_degree(n)})' for n in top_depended]}")
    print(f"{'='*40}\n")

    # Legend
    legend = [
        mpatches.Patch(color="#f28b82", label="In a cycle (circular dependency)"),
        mpatches.Patch(color="#aecbfa", label="Heavily depended-upon (≥3 incoming)"),
        mpatches.Patch(color="#fdd663", label="High coupling (≥3 outgoing)"),
        mpatches.Patch(color="#a8d8a8", label="Isolated / leaf class"),
        mpatches.Patch(color="#e0e0e0", label="Normal"),
    ]
    ax.legend(handles=legend, loc="upper left", fontsize=8)

    plt.title("Class Dependency Graph", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    project_dir = "Original"
    classes, edges = build_class_graph(project_dir)
    draw_graph(classes, edges)