from typing import List


def graph_from_csv(csv: str) -> List[List]:
    csv_edges = [edge.split(",") for edge in csv.split("\n")]
    vertex_neighboors = {}
    vertexes = set()
    for edge in csv_edges:
        vertexes.add(edge[0])
        vertexes.add(edge[1])
        if vertex_neighboors.get(edge[0]):
            vertex_neighboors[edge[0]].append(edge[1])
        else:
            vertex_neighboors[edge[0]] = [edge[1]]
    graph = []
    for vertex_out in sorted(list(vertexes)):
        row = [0] * len(vertexes)
        neighboors = (
            vertex_neighboors.get(vertex_out)
            if vertex_neighboors.get(vertex_out)
            else []
        )
        for vertex_in in sorted(neighboors):
            row[int(vertex_in) - 1] = 1 if vertex_in in neighboors else False
        graph.append(row)
    return graph

def root_vertex_from_csv(csv: str):
    return int([edge.split(",") for edge in csv.split("\n")][0][0])


# ector < vector<int> > g; // граф
# int n; // число вершин

# vector<char> used;

# void dfs (int v) {
# 	used[v] = true;
# 	for (vector<int>::iterator i=g[v].begin(); i!=g[v].end(); ++i)
# 		if (!used[*i])
# 		    dfs (*i);
#}

def dfs(g, used, v):
    used[v] = 1
    for i in range(len(g[v])):
        if not used[i]:
            if g[v][i]:
                dfs(g, used, i)
    return used

def main(csv: str):
    g = graph_from_csv(csv)
    n = len(g[0])
    empty = [[0 for _ in range(n)] for _ in range(n)]
    root_vertex = root_vertex_from_csv(csv)
    r1 = g
    r2 = []
    for i in range(n):
        r2.append([row[i] for row in g])
    r3 = [dfs(g, [0 for i in range(n)], j) for j in range(n)]
    r4 = []
    for i in range(n):
        r4.append([row[i] for row in r3])
    r5 = empty.copy()
    for i in range(n):
        for j in range(n):
            r5[i][j] = 1 if r3[i][j] and r3[j][i] else 0
    return (r1, r2, r3, r4, r5)



for t in main("1,2\n1,3\n3,4\n3,5\n5,6\n6,7"):
    for l in t:
        print(l)
    print()
