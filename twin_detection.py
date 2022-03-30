from graph_io import *


def count_twins(G: Graph):
    all_twins = []
    for vertex in G.vertices:
        twins = []
        for other_vertex in G.vertices:
            if vertex == other_vertex:
                continue
            vertex_neighbourhood = set(vertex.neighbours[:])
            other_vertex_neighbourhood = set(other_vertex.neighbours[:])
            if other_vertex in vertex_neighbourhood:
                vertex_neighbourhood.remove(other_vertex)
            if vertex in other_vertex_neighbourhood:
                other_vertex_neighbourhood.remove(vertex)
            if vertex_neighbourhood == other_vertex_neighbourhood:
                if any(vertex in sl for sl in all_twins):
                    break
                elif vertex in twins:
                    twins.append(other_vertex)
                else:
                    twins.append(vertex)
                    twins.append(other_vertex)
        if twins:
            all_twins.append(twins)
    return all_twins


"""
G = Graph(True, n=5)
G.add_edge(Edge(G.vertices[0], G.vertices[1]))
G.add_edge(Edge(G.vertices[1], G.vertices[2]))
G.add_edge(Edge(G.vertices[0], G.vertices[3]))
G.add_edge(Edge(G.vertices[3], G.vertices[2]))
G.add_edge(Edge(G.vertices[0], G.vertices[4]))
G.add_edge(Edge(G.vertices[4], G.vertices[2]))
G.add_edge(Edge(G.vertices[4], G.vertices[3]))

with open('graphs/results/example.gr', 'w') as f:
    save_graph(G,f)

with open('graphs/results/example.dot', 'w') as f:
    write_dot(G,f)

with open('graphs/wheeljoin14.grl') as f:
    graph_list = load_graph(f, read_list=True)

H = graph_list[0][0]

    
test = count_twins(H)
print(test)
"""