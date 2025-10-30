from typing import List, Tuple
import csv
import math
from collections import defaultdict

def parse_csv(s: str) -> List[Tuple[str, str]]:
    reader = csv.reader(s.splitlines())
    return [(row[0].strip(), row[1].strip()) for row in reader]

def build_graph(edges: List[Tuple[str, str]]) -> dict:
    graph = defaultdict(list)
    for parent, child in edges:
        graph[parent].append(child)
    return graph

def calculate_entropy(graph: dict, root: str) -> float:
    if root not in graph:
        return 0.0

    def dfs(node: str) -> int:
        if node not in graph or not graph[node]:
            return 1
        size = 1
        for child in graph[node]:
            size += dfs(child)
        return size

    subtree_sizes = []
    for node in graph:
        subtree_sizes.append(dfs(node))

    total_nodes = sum(subtree_sizes)
    probabilities = [size / total_nodes for size in subtree_sizes]

    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

def normalized_structural_complexity(graph: dict) -> float:
    edge_count = sum(len(children) for children in graph.values())
    node_count = len(graph)
    if node_count <= 1:
        return 0.0

    complexity = edge_count / (node_count * (node_count - 1))
    return complexity

def task(s: str, root: str) -> Tuple[float, float]:
    edges = parse_csv(s)

    graph = build_graph(edges)

    entropy = calculate_entropy(graph, root)

    complexity = normalized_structural_complexity(graph)

    return (round(entropy, 1), round(complexity, 1))
