from typing import List


def main(csv : str) -> List[List]:
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
    print(vertexes)
    graph = []
    for vertex_out in vertexes:
        row = [0] * len(vertexes)
        neighboors = vertex_neighboors.get(vertex_out) if vertex_neighboors.get(vertex_out) else []
        for index, vertex_in in enumerate(vertexes):
            row[index] = 1 if vertex_in in neighboors else 0
        graph.append(row)
    return graph

for row in main("1,2\n1,3\n3,4\n3,5"):
    print(row)

